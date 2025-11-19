with open ("export.xml", "r") as file:
    data = file.readlines()
print(len(data))

with open ("smaller.xml", "w") as file:
    file.writelines(data[:30000])