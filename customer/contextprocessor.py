from eKart_admin.models import Category

def getCategory(self):
    categoryList=Category.objects.all()

    return dict(categoryList=categoryList)