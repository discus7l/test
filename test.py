######------------ Original Script ------------######
# import sheetControl

# response = sheetControl.myFunction()
# print(response)

######------------ In folder ------------######
# from locPack import sheetControl

# response = sheetControl.myFunction()
# print(response)

######------------ In folder /w __init__.py ------------######
# With init.py we can call the function within the module within the package in short calls
# virtually skipping the module name
# "package.func" rather than "package.module.function"
# from locPack.sheetControl import myFunction as func
import locPack

response = locPack.func()
print(response)
