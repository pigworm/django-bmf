from .testcases import BMFViewTestCase as ViewTestCase
from .testcases import BMFModuleTestCase as ModuleTestCase
from .testcases import BMFWorkflowTestCase as WorkflowTestCase

from djangobmf.utils.deprecation import RemovedInNextBMFVersionWarning

import warnings


class BMFViewTestCase(ViewTestCase):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "djangobmf.testcase is is deprecated - use djangobmf.testcases",
            RemovedInNextBMFVersionWarning, stacklevel=2)
        super(BMFViewTestCase, self).__init__(*args, **kwargs)


class BMFModuleTestCase(ModuleTestCase):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "djangobmf.testcase is is deprecated - use djangobmf.testcases",
            RemovedInNextBMFVersionWarning, stacklevel=2)
        super(BMFModuleTestCase, self).__init__(*args, **kwargs)


class BMFWorkflowTestCase(WorkflowTestCase):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "djangobmf.testcase is is deprecated - use djangobmf.testcases",
            RemovedInNextBMFVersionWarning, stacklevel=2)
        super(BMFWorkflowTestCase, self).__init__(*args, **kwargs)
