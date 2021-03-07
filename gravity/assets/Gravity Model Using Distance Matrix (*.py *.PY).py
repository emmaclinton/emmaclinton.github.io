"""
Model exported as python.
Name : Gravity Model Using Distance Matrix
Group : MIddlebury
With QGIS : 31604
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSource
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterDefinition
from qgis.core import QgsExpression
import processing


class GravityModelUsingDistanceMatrix(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource('InputFeatures', 'Input Features', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('InputID', 'Input ID', type=QgsProcessingParameterField.Any, parentLayerParameterName='InputFeatures', allowMultiple=False, defaultValue=''))
        self.addParameter(QgsProcessingParameterFeatureSource('TargetFeatures', 'Target Features', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('TargetID', 'Target ID', type=QgsProcessingParameterField.Any, parentLayerParameterName='TargetFeatures', allowMultiple=False, defaultValue=''))
        self.addParameter(QgsProcessingParameterField('TargetWeight', 'Target Weight', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='TargetFeatures', allowMultiple=False, defaultValue=''))
        param = QgsProcessingParameterNumber('Alpha', 'Alpha', type=QgsProcessingParameterNumber.Integer, minValue=1, defaultValue=1)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterNumber('Beta', 'Beta', type=QgsProcessingParameterNumber.Integer, minValue=1, defaultValue=2)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        self.addParameter(QgsProcessingParameterField('InputWeightField', 'Input Weight Field', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='InputFeatures', allowMultiple=False, defaultValue=''))
        param = QgsProcessingParameterNumber('Lambda', 'Lambda', type=QgsProcessingParameterNumber.Integer, minValue=1, defaultValue=1)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterNumber('k', 'k', type=QgsProcessingParameterNumber.Double, minValue=1, maxValue=1.79769e+308, defaultValue=20)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        self.addParameter(QgsProcessingParameterFeatureSink('Aggregate', 'Aggregate', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extracted', 'Extracted', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Gt', 'gt', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('HospitalCatchmentsPopulatedAreas', 'Hospital Catchments (Populated Areas)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Potential', 'Potential', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('DistanceMatrixOutput', 'Distance Matrix Output', type=QgsProcessing.TypeVectorPoint, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(14, model_feedback)
        results = {}
        outputs = {}

        # Extract by expression (input > 0)
        alg_params = {
            'EXPRESSION': QgsExpression('@InputWeightField + \'>0\'').evaluate(),
            'INPUT': parameters['InputFeatures'],
            'OUTPUT': parameters['Gt']
        }
        outputs['ExtractByExpressionInput0'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Gt'] = outputs['ExtractByExpressionInput0']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Extract by expression target
        alg_params = {
            'EXPRESSION': '@TargetWeight + \'>0\'',
            'INPUT': parameters['TargetFeatures'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByExpressionTarget'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Target Centroids
        alg_params = {
            'ALL_PARTS': False,
            'INPUT': outputs['ExtractByExpressionTarget']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['TargetCentroids'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Input Centroids
        alg_params = {
            'ALL_PARTS': False,
            'INPUT': outputs['ExtractByExpressionInput0']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['InputCentroids'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Distance matrix
        alg_params = {
            'INPUT': outputs['InputCentroids']['OUTPUT'],
            'INPUT_FIELD': parameters['InputID'],
            'MATRIX_TYPE': 0,
            'NEAREST_POINTS': parameters['k'],
            'TARGET': outputs['TargetCentroids']['OUTPUT'],
            'TARGET_FIELD': parameters['TargetID'],
            'OUTPUT': parameters['DistanceMatrixOutput']
        }
        outputs['DistanceMatrix'] = processing.run('qgis:distancematrix', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['DistanceMatrixOutput'] = outputs['DistanceMatrix']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Join input weight to distance matrix by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'InputID',
            'FIELDS_TO_COPY': parameters['InputWeightField'],
            'FIELD_2': parameters['InputID'],
            'INPUT': outputs['DistanceMatrix']['OUTPUT'],
            'INPUT_2': parameters['InputFeatures'],
            'METHOD': 1,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinInputWeightToDistanceMatrixByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Join target weight by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'TargetID',
            'FIELDS_TO_COPY': parameters['TargetWeight'],
            'FIELD_2': parameters['TargetID'],
            'INPUT': outputs['JoinInputWeightToDistanceMatrixByFieldValue']['OUTPUT'],
            'INPUT_2': parameters['TargetFeatures'],
            'METHOD': 1,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinTargetWeightByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Field calculator potential
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'potential',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': QgsExpression('(@InputWeightField + \'^\' + to_string(@Lambda) + \'*\' +  @TargetWeight + \'^\' + to_string(@Alpha) ) + (\' / (\"Distance\"/1000)^\' + to_string(@Beta))').evaluate(),
            'INPUT': outputs['JoinTargetWeightByFieldValue']['OUTPUT'],
            'OUTPUT': parameters['Potential']
        }
        outputs['FieldCalculatorPotential'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Potential'] = outputs['FieldCalculatorPotential']['OUTPUT']

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Maximum Potential
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'maxpotential',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'maximum(\"potential\", group_by:= \"InputID\")',
            'INPUT': outputs['FieldCalculatorPotential']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MaximumPotential'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Extract by expression (Potential > 0)
        alg_params = {
            'EXPRESSION': '\'potential\'+ \'>0\'',
            'INPUT': outputs['MaximumPotential']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByExpressionPotential0'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Extract by expression (Max Potential)
        alg_params = {
            'EXPRESSION': '\"potential\" = \"maxpotential\" AND \"maxpotential\" > 0 ',
            'INPUT': outputs['MaximumPotential']['OUTPUT'],
            'OUTPUT': parameters['Extracted']
        }
        outputs['ExtractByExpressionMaxPotential'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extracted'] = outputs['ExtractByExpressionMaxPotential']['OUTPUT']

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Join max potential to towns
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['InputID'],
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'InputID',
            'INPUT': parameters['InputFeatures'],
            'INPUT_2': outputs['ExtractByExpressionMaxPotential']['OUTPUT'],
            'METHOD': 1,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinMaxPotentialToTowns'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Aggregate
        alg_params = {
            'AGGREGATES': [{'aggregate': 'first_value','delimiter': ',','input': 'TargetID','length': 0,'name': 'TargetID','precision': 0,'type': 10},{'aggregate': 'first_value','delimiter': ',','input': 'attribute(@TargetWeight)','length': 0,'name': 'TargetWeight','precision': 0,'type': 4},{'aggregate': 'sum','delimiter': ',','input': 'attribute(@InputWeightField)','length': 0,'name': 'SumInputWeight','precision': 0,'type': 4}],
            'GROUP_BY': 'TargetID',
            'INPUT': outputs['JoinMaxPotentialToTowns']['OUTPUT'],
            'OUTPUT': parameters['Aggregate']
        }
        outputs['Aggregate'] = processing.run('native:aggregate', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Aggregate'] = outputs['Aggregate']['OUTPUT']

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Extract by expression (Non-Null Values)
        alg_params = {
            'EXPRESSION': QgsExpression('\'SumInputWeight\' + \'> 0\'').evaluate(),
            'INPUT': outputs['Aggregate']['OUTPUT'],
            'OUTPUT': parameters['HospitalCatchmentsPopulatedAreas']
        }
        outputs['ExtractByExpressionNonnullValues'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['HospitalCatchmentsPopulatedAreas'] = outputs['ExtractByExpressionNonnullValues']['OUTPUT']
        return results

    def name(self):
        return 'Gravity Model Using Distance Matrix'

    def displayName(self):
        return 'Gravity Model Using Distance Matrix'

    def group(self):
        return 'MIddlebury'

    def groupId(self):
        return 'MIddlebury'

    def createInstance(self):
        return GravityModelUsingDistanceMatrix()
