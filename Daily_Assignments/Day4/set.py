pan_numbers = ["ABCDE1234F", "PQRSX5678K", "ABCDE1234F", "LMNOP9876Q","LMNOP9876Q"]

if len(pan_numbers) != len(set(pan_numbers)):
    print(" Duplicate PAN numbers found in upload sheet!") 
    duplicates = [pan for pan in set(pan_numbers) if pan_numbers.count(pan) > 1]
    print(duplicates)