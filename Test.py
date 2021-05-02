import json
import ast
import unittest
from appium import webdriver

class TestsCalculator(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # set up appium
        desired_caps = {}
        desired_caps["app"] = "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App"
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            desired_capabilities=desired_caps)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def getresults(self):
        # this func get the res from the win calc
        displaytext = self.driver.find_element_by_accessibility_id("CalculatorResults").text
        displaytext = displaytext.strip("Display is ")
        # displaytext = displaytext.rstrip(' ')
        # displaytext = displaytext.lstrip(' ')
        return displaytext

    def numstr(self, arr):
        # this func convert num/action to a word - command calc
        a = []
        for num in arr:
            d = {0: 'Zero', 1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five',
                 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', '+': 'Plus', '-': 'Minus', '*': 'Multiply by',
                 '/': 'Divide by', '=': 'Equals'}
            a.append(d[num])
        return (a)

    def numtow(self, num, equal):
        # this func get array and do 2 action
        # 1 check if i is int and make 44 to 4,4 , if not and i is str append i
        arr = []
        for i in num:
            if isinstance(i, int):
                arr.append(list(map(int, str(i))))
            elif isinstance(i, str):
                arr.append(i)
        targil = []
        # 2 take the array arr =[[2,3],"+",[3],"="] to new array targil => [2,3,'+',3,'=']
        for i in arr:
            if (type(i) != list):
                targil.append(i)
            else:
                for j in i:
                    targil.append(j)
        # print(targil)
        targil = self.numstr(targil)
        self.jsoncalc(targil, equal)

    def test_json_file(self):
        with open('Targilim.json') as f:
            data = json.load(f)
            jsonarry = json.dumps(data['targilim'])
            array = json.loads(jsonarry)
            for i in array:
                # targil is str obj
                targil = json.dumps(i)
                # convert targil to a dict obj
                todict = ast.literal_eval(targil)
                # get dict val
                dictval = list(todict.values())
                equal = str(dictval[-1])
                # print(type(equal))
                dictval = dictval[:-1]
                dictval.append('=')
                self.numtow(dictval, equal)

    def jsoncalc(self, arr, equal):
        for i in arr:
            self.driver.find_element_by_name(i).click()
        return self.assertEqual(self.getresults(), equal)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestsCalculator)
    unittest.TextTestRunner(verbosity=2).run(suite)
