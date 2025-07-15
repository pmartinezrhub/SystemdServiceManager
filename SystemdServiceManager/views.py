from django.shortcuts import render
import subprocess
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest

import subprocess

def get_services():
    result = subprocess.run(
        ['systemctl', 'list-units', '--type=service', '--all', '--no-pager', '--no-legend'],
        stdout=subprocess.PIPE,
        text=True
    )
    services = []
    for line in result.stdout.strip().split('\n'):
        parts = line.split(None, 4)
        if len(parts) == 5:
            name, loaded, state, substate, description = parts

            enabled_result = subprocess.run(
                ['systemctl', 'is-enabled', name],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True
            )
            enabled_state = enabled_result.stdout.strip()  

            services.append({
                'name': name,
                'description': description,
                'state': state,
                'enabled': enabled_state
            })
    return services


def home(request):
    query = request.GET.get('q', '').lower()
    all_services = get_services()
    
    if query:
        filtered_services = [
            s for s in all_services
            if query in s['name'].lower() or query in s['description'].lower()
        ]
    else:
        filtered_services = all_services

    return render(request, 'home.html', {'services': filtered_services})


@require_POST
def start_service(request):
    service_name = request.POST.get("service_name")

    if not service_name:
        return HttpResponseBadRequest("Service name is required.")

    try:
        subprocess.run(["systemctl", "start", service_name], check=True)
    except subprocess.CalledProcessError:
        return HttpResponseBadRequest("Failed to start service.")

    return redirect('home') 

@require_POST
def restart_service(request):
    service_name = request.POST.get("service_name")

    if not service_name:
        return HttpResponseBadRequest("Service name is required.")

    try:
        subprocess.run(["systemctl", "restart", service_name], check=True)
    except subprocess.CalledProcessError:
        return HttpResponseBadRequest("Failed to restart service.")

    return redirect('home') 

@require_POST
def stop_service(request):
    service_name = request.POST.get("service_name")

    if not service_name:
        return HttpResponseBadRequest("Service name is required.")

    try:
        subprocess.run(["systemctl", "stop", service_name], check=True)
    except subprocess.CalledProcessError:
        return HttpResponseBadRequest("Failed to stop service.")

    return redirect('home') 

@require_POST
def enable_service(request):
    service_name = request.POST.get("service_name")

    if not service_name:
        return HttpResponseBadRequest("Service name is required.")

    try:
        subprocess.run(["systemctl", "enable", service_name], check=True)
    except subprocess.CalledProcessError:
        return HttpResponseBadRequest("Failed to enable service.")

    return redirect('home') 

@require_POST
def disable_service(request):
    service_name = request.POST.get("service_name")

    if not service_name:
        return HttpResponseBadRequest("Service name is required.")

    try:
        subprocess.run(["systemctl", "disable", service_name], check=True)
    except subprocess.CalledProcessError:
        return HttpResponseBadRequest("Failed to disable service.")

    return redirect('home') 