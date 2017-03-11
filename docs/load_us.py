import csv

f = open('docs/us_guestlist.csv',encoding = "utf-16")
us_list = csv.DictReader(f)

guests = [
	Guest(
		name = row['name'],
		address1 = row['address_1'],
		address2 = row['address_2'],
		city = row['city'],
		state = row['state'],
		country = row['country'],
		zipcode = row['zipcode'],
		wedding_code = row['wedcode']
		) for row in us_list]

print(guests)
Guest.objects.bulk_create(guests)
