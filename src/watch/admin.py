from django.contrib import admin

# Register your models here.
from models import Asset


class AssetAdmin(admin.ModelAdmin):
    list_display=('sn','mac','type')

admin.site.register(Asset, AssetAdmin)