import pandas as pd
import tkinter as tk
from tkinter import ttk

#Armor class
class Armor:
    #Constructor
    def __init__(self, type, rank, name, defense, lvl1GemSlot, lvl2GemSlot, lvl3GemSlot, lvl4GemSlot, fireRes, waterRes, thunderRes, iceRes, dragonRes, skillDict):
        self.armorType = type
        self.rank = rank
        self.name = name
        self.defense = defense
        self.lvl1GemSlot = lvl1GemSlot
        self.lvl2GemSlot = lvl2GemSlot
        self.lvl3GemSlot = lvl3GemSlot
        self.lvl4GemSlot = lvl4GemSlot
        self.fireRes = fireRes
        self.waterRes = waterRes
        self.thunderRes = thunderRes
        self.iceRes = iceRes
        self.dragonRes = dragonRes
        self.skillDict = skillDict
    
    def is_skill_in_armor(self, skillName):
        return skillName in self.skillDict
    


skillDF= pd.read_csv(r"c:\Users\Godoy\OneDrive - Fatec Centro Paula Souza\mhrs_skills.csv")
armorDF = pd.read_csv(r"c:\Users\Godoy\OneDrive - Fatec Centro Paula Souza\mhrs_mr_armors.csv")

armorDFColumnList = []

for item in armorDF.columns[1:]:
    armorDFColumnList.append(item)


headObjList = []
chestObjList = []
gauntletObjList = []
waistObjList = []
legObjList = []

headNameList = []
chestNameList = []
gauntletNameList = []
waistNameList = []
legNameList = []


for index, row in armorDF.iterrows():
    
    newArmorSkillDict = {}
    for c in armorDFColumnList[13:]:
        if row[c] != 0:
            newArmorSkillDict[c] = row[c]
        else:
            pass

    newArmorObj = Armor(
        row[armorDFColumnList[0]],
        row[armorDFColumnList[1]],
        row[armorDFColumnList[2]],
        row[armorDFColumnList[3]],
        row[armorDFColumnList[4]],
        row[armorDFColumnList[5]],
        row[armorDFColumnList[6]],
        row[armorDFColumnList[7]],
        row[armorDFColumnList[8]],
        row[armorDFColumnList[9]],
        row[armorDFColumnList[10]],
        row[armorDFColumnList[11]],
        row[armorDFColumnList[12]],
        newArmorSkillDict
    )

    match(newArmorObj.armorType):
        case 0:
            headObjList.append(newArmorObj)
            headNameList.append(newArmorObj.name)
        case 1:
            chestObjList.append(newArmorObj)
            chestNameList.append(newArmorObj.name)
        case 2:
            gauntletObjList.append(newArmorObj)
            gauntletNameList.append(newArmorObj.name)
        case 3:
            waistObjList.append(newArmorObj)
            waistNameList.append(newArmorObj.name)
        case 4:
            legObjList.append(newArmorObj)
            legNameList.append(newArmorObj.name)



def print_to_label(lbl, cbox):
    lbl["text"] = cbox.get()

root = tk.Tk()

frmArmors = ttk.Frame(root)
frmArmors.grid(row=0, column=0)


cmbHelmCombo = ttk.Combobox(frmArmors, values=headNameList)
cmbHelmCombo.pack()

cmbChestCombo = ttk.Combobox(frmArmors, values=chestNameList)
cmbChestCombo.pack()

cmbGauntletCombo = ttk.Combobox(frmArmors, values=gauntletNameList)
cmbGauntletCombo.pack()

cmbWaistCombo = ttk.Combobox(frmArmors, values=waistNameList)
cmbWaistCombo.pack()

cmbLegCombo = ttk.Combobox(frmArmors, values=legNameList)
cmbLegCombo.pack()





root.mainloop()

'''
lblLabel = ttk.Label(root, text="I'm a Label !")
lblLabel.pack()

btnButton = ttk.Button(root, text="I'm a BUtton !")
btnButton.pack()

cnvCanvas= tk.Canvas(root)
cnvCanvas.pack()

numList = [1,2,3,4,5,6]
cmbComboBox = ttk.Combobox(root, values=numList)
cmbComboBox.pack()

ckbCheckButton = ttk.Checkbutton(root, text="Check1")
ckbCheckButton.pack()
ckbCheckButton2 = ttk.Checkbutton(root, text="Check2")
ckbCheckButton2.pack()

rdbRadioButton = ttk.Radiobutton(root, text="Radio1")
rdbRadioButton.pack()
rdbRadioButton2 = ttk.Radiobutton(root, text="Radio2")
rdbRadioButton2.pack()

sclScale = ttk.Scale(root, from_= 0, to=10)
sclScale.pack()

lblScaleLabel = ttk.Label(root)
lblScaleLabel.pack()

entEntry = ttk.Entry(root)
entEntry.pack()

sbrScrollBar = ttk.Scrollbar(root)
sbrScrollBar.pack()

spnSpinBox = ttk.Spinbox(root)
spnSpinBox.pack()

#mnuMenu = tk.Menu(root)
#mnuMenu.pack()
'''