from django.contrib import admin
from .models import FarmerEntry, MillEntry,HarvestFarmer


from django.contrib import admin
from .models import FarmerEntry


@admin.register(FarmerEntry)
class FarmerEntryAdmin(admin.ModelAdmin):

    # 🔍 SEARCH FIELDS
    search_fields = [
            '^farmer_name', 
            '^district',
            '^mobile',
            '^acres',
            '^total_bags',
            '^total_amount', # starts with
            '^village',
            '^crop_type',
            '^lorry_number',
            
    ]

    # 📋 DISPLAY IN TABLE (optional but useful)
    list_display = [
            'farmer_name',
            'district',
            'mobile',
            'acres',
            'total_bags',
            'total_amount',
            'village',
            'crop_type',
            'lorry_number',
            
        
    ]

@admin.register(MillEntry)
class MillAdmin(admin.ModelAdmin):
    search_fields = ['^owner_name',
                      '^mill_name', 
                      '^district',
                      '^mill_address',
                      '^mobile',
                      '^bags',
                      '^amount',
                      '^paddy_type',
                     '^lorry',
                     '^image'
    ]
    list_display = ['owner_name',
                      'mill_name', 
                      'district',
                      'mill_address',
                      'mobile',
                      'bags',
                      'amount',
                      'paddy_type',
                      'lorry',
                      'image'
    ]

@admin.register(HarvestFarmer)
class HarvestFarmerAdmin(admin.ModelAdmin):
    search_fields = [
        '^farmer_name',
        '^village',
        '^state',
        '^phone',
        '^date',
        '^operator_name',
        '^machine_number',
        '^acres',
        
        '^amount'
    ]
    list_display = [
        'farmer_name',
        'village',
        'state',
        'phone',
        'date',
        'operator_name',
        'machine_number',
        'acres',
        
        'amount'
              
    ]

from .models import HarvesterOperator

@admin.register(HarvesterOperator)
class HarvesterOperatorAdmin(admin.ModelAdmin):
    list_display = [
        'operator_name',
        'machine_number',
        'date',
        'farmer_name',
        'village',
        'acres',
        'total_time',
        'total_amount'
    ]

    search_fields = [
        '^operator_name',
        '^machine_number',
        '^date',
        '^farmer_name',
        '^village',
        '^acres',
        '^total_time',
        '^total_amount'
    ]
    list_filter = ['date']

    date_hierarchy = 'date'   # 🔥 Calendar navigation
    
admin.site.site_header = "Prasad Reddy Paddy Aggregation Admin"
admin.site.site_title = "Aggregation Admin Portal"
admin.site.index_title = "Welcome to Paddy Aggregation Dashboard"











