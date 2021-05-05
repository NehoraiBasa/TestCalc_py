import unittest

class ParametrizedTestCase(unittest.TestCase):
    # TestCase classes that want to be parametrized should inherit from this class.


    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param
        self.e =[]


    @staticmethod
    def parametrize(testcase_klass, param=None):
     # Create a suite containing all tests taken from the given subclass, passing them the parameter 'param'.
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite

class TestOne(ParametrizedTestCase):
    def test_something(self):
        self.e.append(5)
        print(self.e)

    def test_something_else(self):
        self.assertEqual(2, 2)


suite = unittest.TestSuite()
suite.addTest(ParametrizedTestCase.parametrize(TestOne, param=42))
suite.addTest(ParametrizedTestCase.parametrize(TestOne, param=13))
unittest.TextTestRunner(verbosity=2).run(suite)

















# import pyautogui, time
#
# pauseSeconds = 1.1
#
# # Open Windows Calculator via CLI
# pyautogui.hotkey('winleft', 'r')
# pyautogui.typewrite('calc', _pause=pauseSeconds)
# pyautogui.press('enter', _pause=pauseSeconds)
#
# # Wait for the Calculator: 2 Seconds
# time.sleep(2)
#
#
# # Addition
# pyautogui.press('escape', _pause=pauseSeconds)
# pyautogui.press('7', _pause=pauseSeconds)
# pyautogui.press('+', _pause=pauseSeconds)
#
#
# pyautogui.press('3', _pause=pauseSeconds)
# pyautogui.press('enter', _pause=pauseSeconds)
#
# # Subtraction
# pyautogui.press('escape', _pause=pauseSeconds)
# pyautogui.press('7', _pause=pauseSeconds)
# pyautogui.press('-', _pause=pauseSeconds)
# pyautogui.press('3', _pause=pauseSeconds)
# pyautogui.press('enter', _pause=pauseSeconds)
#
# # Multiplication
# pyautogui.press('escape', _pause=pauseSeconds)
# pyautogui.press('7', _pause=pauseSeconds)
# pyautogui.press('*', _pause=pauseSeconds)
# pyautogui.press('3', _pause=pauseSeconds)
# pyautogui.press('enter', _pause=pauseSeconds)
#
# # Division
# pyautogui.press('escape', _pause=pauseSeconds)
# pyautogui.press('7', _pause=pauseSeconds)
# pyautogui.press('/', _pause=pauseSeconds)
# pyautogui.press('3', _pause=pauseSeconds)
# pyautogui.press('enter', _pause=pauseSeconds)
#
# # Close Calculator
# pyautogui.press('escape', _pause=pauseSeconds)
# pyautogui.hotkey('alt', 'f4')