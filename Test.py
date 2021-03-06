import json
import ast
import unittest
from appium import webdriver

class TestsCalculator(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super(TestsCalculator, self).__init__(methodName)
        self.plus = []
        self.Equalplus = 0
        self.minus = []
        self.Equalminus = 0
        self.division = []
        self.Equaldivision = 0
        self.multiply = []
        self.Equalmultiply = 0
        self.combination = []
        self.Equalcombination = 0

        with open('Targilim.json') as f:
            data = json.load(f)
            targilim_json_arry = json.dumps(data['targilim'])
            targilim_array = json.loads(targilim_json_arry)
            for i in targilim_array:
                # targil is str obj
                targil = json.dumps(i)
                # convert targil to a dict obj
                targil_todict = ast.literal_eval(targil)
                # get dict val
                targil_dict_values = list(targil_todict.values())
                equal = str(targil_dict_values[-1])
                targil_dict_values = targil_dict_values[:-1]
                targil_dict_values.append('=')
                self.TypeTargil(targil_dict_values,equal)


    @classmethod
    def setUpClass(self):
        #set up appium
        desired_caps = {}
        desired_caps["app"] = "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App"
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            desired_capabilities=desired_caps)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()


    def TypeTargil(self,targil_dict_values,equal):
        # this func puts each targil into its own arr
        get_targil = self.GetTargil(targil_dict_values)
        exercise_type = self.ExerciseType(get_targil)
        if exercise_type == "Plus":
            self.plus.append(get_targil)
            self.Equalplus = equal
        elif exercise_type == "Minus":
            self.minus.append(get_targil)
            self.Equalminus = equal
        elif exercise_type == "Multiply by":
            self.multiply.append(get_targil)
            self.Equalmultiply = equal
        elif exercise_type == "Divide by":
            self.division.append(get_targil)
            self.Equaldivision = equal
        elif exercise_type == "Combiation":
            self.combination.append(get_targil)
            self.Equalcombination = equal



    def GetTargil(self, arrTargil):
        arr = self.TargilArray(arrTargil)
        arr_targil = self.Targil(arr)
        return arr_targil


    def GetResult(self):
        #this func get the res from the win calc
        displaytext = self.driver.find_element_by_accessibility_id("CalculatorResults").text
        displaytext = displaytext.strip("Display is ")
        return displaytext


    def CommandCalc(self, targil):
        # this func convert num/action to a word - command calc
        command = []
        d = {0: 'Zero', 1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five',
             6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', '+': 'Plus', '-': 'Minus', '*': 'Multiply by',
             '/': 'Divide by', '=': 'Equals'}
        for i in targil:
            command.append(d[i])
        return command


    def TargilArray(self,arrTargil):
        # this func  get array and check if i is int and make 44 to 4,4 , if not and i is str append i
        arr = []
        for i in arrTargil:
            if isinstance(i, int):
                arr.append(list(map(int, str(i))))
            elif isinstance(i, str):
                arr.append(i)
        return arr


    def Targil(self,targilarr):
        # this func take the array targilarr =[[2,3],"+",[3],"="] to new array arr_targil => [2,3,'+',3,'=']
        arr_targil = []
        for i in targilarr:
            if (type(i) != list):
                arr_targil.append(i)
            else:
                for j in i:
                    arr_targil.append(j)
        targil = self.CommandCalc(arr_targil)
        return targil


    def ExerciseType(self, arr):
        a = 0
        action = ""
        for i in arr:
            if i == "Plus" or i == "Minus" or i == "Multiply by" or i =='Divide by':
                a += 1
                if(a > 1):
                    return ("Combiation")
                action = i
        return action


    def RunCalc(self, arrTargil):
        # this func executes the calc commands
        for targil in arrTargil:
            for i in targil:
                self.driver.find_element_by_name(i).click()
        return self.GetResult()




class Testes(TestsCalculator):

    def test_minus(self):
        targil = self.minus
        equal = self.Equalminus
        self.RunCalc(targil)
        self.assertEqual(self.GetResult(), equal)

    def test_plus(self):
        targil=self.plus
        equal=self.Equalplus
        self.RunCalc(targil)
        self.assertEqual(self.GetResult(), equal)

    def test_multiplication(self):
        targil = self.multiply
        equal = self.Equalmultiply
        self.RunCalc(targil)
        self.assertEqual(self.GetResult(), equal)

    def test_division(self):
        targil = self.division
        equal = self.Equaldivision
        self.RunCalc(targil)
        self.assertEqual(self.GetResult(), equal)

    def test_combination(self):
        targil = self.combination
        equal = self.Equalcombination
        self.RunCalc(targil)
        self.assertEqual(self.GetResult(), equal)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Testes)
    unittest.TextTestRunner(verbosity=1).run(suite)