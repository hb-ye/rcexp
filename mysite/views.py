# Create your views here.

"""
import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from . import database
from .models import PageView
"""

import os.path
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
import datetime
import random
import json
# from time import sleep
import numpy as np

from mysite.forms import Game_Info, Route_Choice #NewExp
from mysite.rcexp.models import Network_Structure, Exp_Info, User_Route_Choice, Path_Flow
from mysite import cal_time


# def home(request):
#     return render_to_response('home.html')
    # return render_to_response('home/home.html')
# from django.template import Template, Context
# from django.template.loader import get_template

def mainpage (request):
    # Exp_Info.objects.all().delete() ######## Must deleted before online
    # User_Route_Choice.objects.all().delete() ######## Must deleted 
    # Path_Flow.objects.all().delete() ######## Must deleted before online
    # print('data cleared')
    link_path_matrix = [[1, 0, 0], [0, 1, 1], [1, 1, 0], [0, 0, 1], [0, 1, 0]]
    link_num = len(link_path_matrix)
    path_num = len(link_path_matrix[0])
    free_flow_time = [25, 10, 5, 20, 15]
    # free_path_time =[]
    link_capacity = [2, 2, 2, 1, 1]
    # link_capacity = [1, 2, 2, 1, 2]
    od_demand = 30

    try:
        p = Network_Structure.objects.get(network_name='Braess_5_link')
    except Network_Structure.DoesNotExist:
        Network_Structure.objects.create(network_name='Braess_5_link', link_path_matrix=json.dumps(link_path_matrix), link_num=link_num, path_num=path_num, free_flow_time=json.dumps(free_flow_time), link_capacity=json.dumps(link_capacity), od_demand=od_demand)
    else:
        p.link_path_matrix=json.dumps(link_path_matrix)
        p.link_num=link_num
        p.path_num=path_num
        p.free_flow_time=json.dumps(free_flow_time)
        p.link_capacity=json.dumps(link_capacity)
        p.od_demand=od_demand
        p.save()

    if request.method == 'POST':
        if 'yes_agree' in request.POST:
            form = Game_Info(request.POST)
            if form.is_valid():
                cd=form.cleaned_data
                user_num = int(cd['user_num'])
                time_interval = int(cd['time_interval'])
                # print('user_num = ', user_num, '\n time_interval = ', time_interval)
                while True:
                    exp_id = str(random.randint(1,9999))
                    exp_id = exp_id.rjust(4, '0')
                    try:
                        p = Exp_Info.objects.get(exp_id=exp_id)
                    except Exp_Info.DoesNotExist:
                        # path_time = [3, 3, 3]
                        # print('create now')
                        path_time = (np.dot(np.array(link_path_matrix).transpose(), np.array(free_flow_time))).tolist()
                        q = Network_Structure.objects.get(network_name='Braess_5_link')
                        Exp_Info.objects.create(exp_id=exp_id, exp_day=1, exp_start=False, exp_fin=False, user_num=0, network_name='Braess_5_link', path_num=q.path_num, current_path_time=json.dumps(path_time), historical_path_time=json.dumps([path_time]), link_path_matrix=q.link_path_matrix, link_num=q.link_num, free_flow_time=q.free_flow_time, od_demand=user_num, link_capacity=json.dumps([i*user_num/3.0 for i in json.loads(q.link_capacity)]), time_interval=time_interval)
                        # print('create ok')
                        break
                        # Exp_Info.objects.create(exp_id=exp_id, exp_day=1, exp_start=False, exp_fin=False, current_num_of_users=0, historical_num_of_users=json.dumps([0]))
                    except:
                        pass
                return HttpResponseRedirect('/RCE/%s/' % exp_id)
            return render_to_response('new_exp.html', {'form': form})
        else:
            return HttpResponseRedirect('http://www.google.com')
    else:
        form = Game_Info()
        return render_to_response('new_exp.html', {'form': form})
    # return render_to_response('new_exp.html')

def route_choice_exp_admin(request, exp_id):
    try:
        p = Exp_Info.objects.get(exp_id=exp_id)
    except Exp_Info.DoesNotExist:
        return HttpResponse('Experiment %s not exist' % exp_id)
    except:
        pass
    else:
        if p.exp_fin:
            return HttpResponseRedirect('/RCE/%s/results' % exp_id)
    
    user_id = 'Admin'
    exp_day = p.exp_day
    exp_addr = str(request.build_absolute_uri()) + 'user'
    current_user_num = p.user_num 
    path_time = json.loads(p.current_path_time)
    path_time_dict=dict([i+1,path_time[i]] for i in range(0,len(path_time)))
    time_interval = p.time_interval

    # if request.method == 'GET':
    #     form = Route_Choice({'exp_id': exp_id, 'user_id': user_id, 'exp_day': exp_day})
    #     return render_to_response('RCE.html', {'exp_id': exp_id, 'user_id': user_id, 'exp_day': exp_day, 'user_num': current_user_num, 'exp_addr': exp_addr, 'form': form})
    if request.method == 'POST':
        # p.historical_num_of_users = json.dumps(historical_user_num)
        # p.user_num = 0
        if 'start_exp' in request.POST:
            p.exp_start = True
            p.user_num = 0
            p.save()
        else:
            path_flow=[]
            for path_id in range(1, p.path_num + 1):
                q = Path_Flow.objects.get(exp_id=exp_id, exp_day=exp_day, path_id=path_id)
                path_flow.append(q.path_flow)
            path_time = cal_time.cal_path_time(path_flow, exp_id)
            path_time = [int(k) for k in path_time]
            path_time_dict=dict([i+1,path_time[i]] for i in range(0,len(path_time)))
            p.current_path_time = path_time
            historical_path_time = json.loads(p.historical_path_time)
            historical_path_time.append(path_time)
            p.historical_path_time = json.dumps(historical_path_time)
            if 'next_step' in request.POST:
                exp_day = exp_day + 1
                p.exp_day = exp_day
                p.user_num = 0
                current_user_num = 0
                p.save()
            else: # 'exit_exp' in request.POST:
                p.exp_fin = True
                p.save()
                return HttpResponseRedirect('/RCE/%s/results' % exp_id)
                # Exp_Info.objects.filter(exp_id=exp_id).update(exp_fin=True)

        p = Exp_Info.objects.get(exp_id=exp_id)
        for path_id in range(1, p.path_num + 1):
            Path_Flow.objects.create(exp_id=exp_id, exp_day=exp_day, path_id=path_id, path_flow=0)

        # Exp_Info.objects.filter(exp_id=exp_id, exp_day=exp_day).update(exp_fin=True)
        # Exp_Info.objects.filter(exp_id=exp_id).update(exp_day=exp_day+1, current)
        # Exp_Info.objects.create(exp_id=exp_id, exp_day=exp_day+1, exp_fin=False, current_num_of_users=0, historical_num_of_users=historical_num_of_users)
        # form = Route_Choice({'exp_id': exp_id, 'user_id': user_id, 'exp_day': exp_day+1})
        # return render_to_response('RCE.html', {'exp_id': exp_id, 'user_id': user_id, 'exp_day': exp_day+1, 'user_num': current_user_num, 'exp_addr': exp_addr, 'form': form})
    if exp_day == 1:
        p = Exp_Info.objects.get(exp_id=exp_id)
        exp_start = p.exp_start
    else:
        exp_start = 1
    form = Route_Choice({'exp_id': exp_id, 'user_id': user_id, 'exp_day': exp_day})
    return render_to_response('RCE.html', {'exp_id': exp_id, 'user_id': user_id, 'exp_day': exp_day, 'user_num': current_user_num, 'exp_addr': exp_addr, 'path_time_dict': path_time_dict, 'exp_start': exp_start, 'time_interval': time_interval, 'form': form})


def route_choice_exp_user(request, exp_id, user_id):
    try:
        p = Exp_Info.objects.get(exp_id=exp_id)
    except Exp_Info.DoesNotExist:
        return HttpResponse('Experiment %s not exist' % exp_id)
    except:
        pass
    else:
        if p.exp_fin:
            return HttpResponseRedirect('/RCE/%s/results' % exp_id)

    if request.is_mobile: #request.is_tablet, request.is_phone)
        is_mobile = True
    else:
        is_mobile = False
    
    exp_start = p.exp_start
    exp_day = int(p.exp_day)
    path_time = json.loads(p.current_path_time)
    path_time_dict=dict([i+1,path_time[i]] for i in range(0,len(path_time)))
    auto_refresh = False
    if not user_id:
        while True:
            user_id = str(random.randint(1,9999))
            user_id = user_id.rjust(4, '0')
            try:
                q = User_Route_Choice.objects.get(exp_id=exp_id, user_id=user_id)
            except User_Route_Choice.DoesNotExist:
                User_Route_Choice.objects.create(exp_id=exp_id, user_id=user_id, exp_day=0, user_choice=0)
                p = Exp_Info.objects.get(exp_id=exp_id)
                if not p.exp_start:
                    p.user_num = p.user_num + 1
                    p.save()
                break
        return HttpResponseRedirect(str(request.build_absolute_uri()) + user_id)
    else:
        try:
            p = User_Route_Choice.objects.get(exp_id=exp_id, user_id=user_id)
        except Exp_Info.DoesNotExist:
            return HttpResponse('User %s not exist' % user_id)
        except:
            pass
        
        if not exp_start:
            form = Route_Choice({'exp_id': exp_id, 'user_id': user_id, 'exp_day': exp_day})
            error_list = ['Game not start, please wait']
            auto_refresh = True
            return render_to_response('RCE.html',{'exp_id': exp_id, 'user_id': user_id, 'exp_day': exp_day, 'path_time_dict': path_time_dict, 'auto_refresh': auto_refresh, 'error_list': error_list, 'is_mobile': is_mobile, 'form': form})

        if request.method == 'GET':
            try:
                p = User_Route_Choice.objects.get(exp_id=exp_id, user_id=user_id, exp_day=exp_day)
            except: #not submit yet
                auto_refresh = False
            else: #already submit
                auto_refresh = True
            form = Route_Choice({'exp_id': exp_id, 'user_id': user_id, 'exp_day': exp_day})
            return render_to_response('RCE.html',{'exp_id': exp_id, 'user_id': user_id, 'exp_day': exp_day, 'path_time_dict': path_time_dict, 'auto_refresh': auto_refresh, 'is_mobile': is_mobile, 'form': form})
        else: #request.method == 'POST':
            error_list=[]
            p =  Exp_Info.objects.get(exp_id=exp_id)
            form = Route_Choice(request.POST)
            if form.is_valid():
                cd=form.cleaned_data
                user_choice = cd['route_choice']
                exp_id = cd['exp_id']
                user_day = int(cd['exp_day'])
                if user_day > exp_day:
                    error_list.append("The day is not comming yet, please choose again")
                    auto_refresh = False
                elif user_day < exp_day:
                    error_list.append("The day has expired, please choose again")
                    auto_refresh = False
                else:
                    user_id = cd["user_id"]
                    try:
                        p = User_Route_Choice.objects.get(exp_id=exp_id, user_id=user_id, exp_day=exp_day)
                    except User_Route_Choice.DoesNotExist: #Correct Submission
                        if user_choice:
                            user_choice = int(user_choice)
                            User_Route_Choice.objects.create(exp_id=exp_id, user_id=user_id, exp_day=exp_day, user_choice=user_choice)
                            p = Path_Flow.objects.get(exp_id=exp_id, exp_day=exp_day, path_id=user_choice)
                            p.path_flow = p.path_flow + 1
                            p.save()
                            q = Exp_Info.objects.get(exp_id=exp_id)
                            q.user_num = q.user_num + 1
                            q.save()
                            auto_refresh = True
                    except:
                        pass
                    else: #the route choice already exists
                        error_list.append("Repeated submission")
                        auto_refresh = True
                    if not user_choice and not error_list:
                        error_list.append("Please choose a route before submit")
                        auto_refresh = False
                        # form = Route_Choice({'exp_id': exp_id, 'user_id': user_id, 'exp_day': exp_day})
                        # return render_to_response('RCE.html',{'exp_id': exp_id, 'user_id': user_id, 'exp_day': exp_day, 'path_time_dict': path_time_dict, 'auto_refresh': auto_refresh, 'form': form})
                            
                            # while True:
                            #     sleep(2)
                            #     p = Exp_Info.objects.get(exp_id=exp_id)
                            #     if p.exp_day != exp_day:
                            #         path_time = json.loads(p.current_path_time)
                            #         path_time_dict=dict([i+1,path_time[i]] for i in range(0,len(path_time)))
                            #         form = Route_Choice({'exp_id': exp_id, 'user_id': user_id, 'exp_day': p.exp_day})
                            #         return render_to_response('RCE.html',{'exp_id': exp_id, 'user_id': user_id, 'exp_day': p.exp_day, 'path_time_dict': path_time_dict, 'auto_refresh': auto_refresh, 'form': form})

            form = Route_Choice({'exp_id': exp_id, 'user_id': user_id, 'exp_day': exp_day})
            return render_to_response('RCE.html', {'exp_id': exp_id, 'user_id': user_id, 'exp_day': exp_day, 'path_time_dict': path_time_dict, 'form': form, 'auto_refresh':auto_refresh, 'error_list': error_list, 'is_mobile': is_mobile})

def publish_results(request, exp_id):
    try:
        p = Exp_Info.objects.get(exp_id=exp_id)
    except Exp_Info.DoesNotExist:
        return HttpResponse('Game not exist')
    except:
        pass
    else:
        historical_path_time = json.loads(p.historical_path_time)
        exp_day = len(historical_path_time)
        path_num = p.path_num
        path_list=['Path '+ str(i) for i in range(1, path_num+1)]
        path_time=[str([i] + historical_path_time[i]) for i in range(0,exp_day)]
        return render_to_response('results.html',{'exp_id': exp_id, 'path_list': path_list, 'path_time': path_time})


		
"""
def index(request):
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'mysite/index.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def health(request):
    return HttpResponse(PageView.objects.count())
"""