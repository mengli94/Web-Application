# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

def calculate(x, y, op):
    if op == '+':
        return x + y
    elif op == '-':
        return x - y
    elif op == '*':
        return x * y
    elif op == '/':
        return x / y

# Create your views here.
def compute(request):
    context = {}
    context = {'display_value': '0', 'last_digit': '', 'curr_digit': '', 'last_op': ''}
    
    if 'display_value' in request.POST:
        context['display_value'] = request.POST['display_value']

    if 'last_digit' in request.POST:
        context['last_digit'] = request.POST['last_digit']
        
    if 'curr_digit' in request.POST:
        context['curr_digit'] = request.POST['curr_digit']
        
    if 'last_op' in request.POST:
        context['last_op'] = request.POST['last_op']
    
    if 'digit' in request.POST:
        digit = request.POST['digit']

        if context['last_op'] == '=':
            context['curr_digit'] = ''
            context['last_digit'] = ''
            context['last_op'] = ''
            
        if context['curr_digit'] != '0':
            context['curr_digit'] += digit
            context['display_value'] = context['curr_digit']
        else :
            context['curr_digit'] = digit
            context['display_value'] = context['curr_digit']
            
    if 'operator' in request.POST:
        operator = request.POST['operator']
            
        try :
            if context['last_op'] == '':
                context['last_digit'] = context['curr_digit']
                context['curr_digit'] = ''
                context['last_op'] = operator
            elif context['last_op'] == '=' :
                context['curr_digit'] = ''
                context['last_op'] = operator
            elif context['curr_digit'] == '' and operator == '-':
                context['curr_digit'] = '-'
            else:
                if context['last_digit'] == '' and context['last_op'] == '-':
                    context['curr_digit'] = calculate(0, int(context['curr_digit']), context['last_op'])
                else :
                    context['curr_digit'] = calculate(int(context['last_digit']), int(context['curr_digit']), context['last_op'])
                
                context['display_value'] = context['curr_digit']
                context['last_digit'] = context['curr_digit']
                context['curr_digit'] = ''
                context['last_op'] = operator
                       
        except ValueError:
                context['curr_digit'] = ''
                context['last_digit'] = ''
                context['last_op'] = ''
                context['display_value'] = "ValueError"
                return render(request, 'calculator.html', context)            

        except ZeroDivisionError:
                context['curr_digit'] = ''
                context['last_digit'] = ''
                context['last_op'] = ''
                context['display_value'] = "ZeroDivisionError"
                return render(request, 'calculator.html', context)    
        
    return render(request, 'calculator.html', context)
        
    
            