import csv
from django.db import migrations


def load_data(apps, schema_editor):
    csv_file_path = '/home/app/datasets/reduced_electronic_products.csv'

    product_model =  apps.get_model("cart", "product")
    primary_category = apps.get_model("cart", "category")
    
    colour_variation = apps.get_model("cart", "colourvariation") 
    size_variation =  apps.get_model("cart", "sizevariation")
    count = 0
    # Leer el CSV
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            count += 1
            # Crear una instancia del modelo Product con los datos del CSV
            main_category_field_value = None
            first_category = row["primaryCategories"]
            
            categories = primary_category.objects.filter(
                name=first_category
            )
            
            if categories.exists():
                main_category_field_value = categories.first()
            else:
                main_category_field_value = primary_category.objects.create(name=first_category)
                
            sub_categories = [
                category.strip() for category in row["Category_name"].split(",")
            ]
    
            # Create categories
            splitted_by_pieces = '-'.join(row['name'].split(' '))
            lowercase = splitted_by_pieces.lower()
            without_signals = lowercase.replace("(", "").replace(")", "").replace("/", "-")
            slug = f"{without_signals}-{count}"
            
            new_product = product_model(
                id=row["id"],
                title=row['name'],
                slug=slug,
                description=row['Description'],
                price=float(row['Actual_price']),
                active=True,
                category_name_encoded=float(row['Category_name_encoded']),
                category_name_encoded_log=float(row['Category_name_encoded_log']),
                currency=row['Currency'],
                country=row['Country'],
                brand=row['brand'],
                brand_standarized=row['brand_standarized'],
                primary_category=main_category_field_value
            )
            
            # options
    
            
            for category in sub_categories:
                
                categories = primary_category.objects.filter(name=category)
                
                if categories.exists():
                    second_category = categories.first()
                    new_product.secondary_categories.add(second_category)
                else:
                    ctg = primary_category.objects.create(name=category)
                    new_product.secondary_categories.add(ctg)
            
            new_product.save()

class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0007_auto_20240414_1744")
    ]

    operations = [
        migrations.RunPython(load_data),
    ]