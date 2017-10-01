from django.db import models

# Create your models here.

class Network_Structure(models.Model):
    # network_default = models.BooleanField(default=True) #False: user-defined
    network_name = models.CharField(max_length=100)
    link_path_matrix = models.CharField(max_length=1000)
    link_num = models.IntegerField()
    path_num = models.IntegerField()
    free_flow_time = models.CharField(max_length=1000)
    link_capacity = models.CharField(max_length=1000)
    od_demand = models.IntegerField()

class Exp_Info(models.Model):
    exp_id = models.CharField(max_length=4)
    exp_day = models.IntegerField()
    exp_start = models.BooleanField(default=False)
    exp_fin = models.BooleanField(default=False)
    user_num = models.IntegerField()
    # network_default = models.BooleanField(default=True)
    network_name = models.CharField(max_length=100)
    path_num = models.IntegerField()
    current_path_time = models.CharField(max_length=100)
    historical_path_time = models.CharField(max_length=100)
    link_path_matrix = models.CharField(max_length=1000)
    link_num = models.IntegerField()
    path_num = models.IntegerField()
    free_flow_time = models.CharField(max_length=1000)
    link_capacity = models.CharField(max_length=1000)
    od_demand = models.IntegerField()
    time_interval = models.IntegerField()
    # historical_num_of_users = models.CharField(max_length=10000)

class User_Route_Choice(models.Model):
    exp_id = models.CharField(max_length=4)
    user_id = models.CharField(max_length=4)
    exp_day = models.IntegerField()
    user_choice = models.IntegerField()

class Path_Flow(models.Model):
    exp_id = models.CharField(max_length=4)
    exp_day = models.IntegerField()
    path_id = models.IntegerField()
    path_flow = models.IntegerField()
    