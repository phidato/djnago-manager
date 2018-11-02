from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView,CreateView, FormView, DeleteView, ListView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.models import UserProfile,UserPost,EmpData,Project,Departments,Designation
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

class SignupView(TemplateView):
	template_name = "app/registrations.html"

		# def post(self, request, *args, **kwargs):
		#     email = request.POST.get('email')
		#     username = request.POST.get('email')
		#     password = request.POST.get('password')

		#     user = User.objects.filter(email=email)
		#     if user:
		#         return HttpResponse('User already exists in the system. Please login instead.')

		#     user = User.objects.create_user(username, email, password)

		#     user.first_name = request.POST.get('first_name')
		#     user.last_name = request.POST.get('last_name')
		#     user.profile.save()
		#     user.save()

		#     login(request, user)
		#     return HttpResponseRedirect('/app/login')

class LoginView(TemplateView):
	template_name = "app/login.html"

class IndexView(TemplateView):
	template_name = "app/index.html"

@csrf_exempt
def save_user(request):
	context = RequestContext(request)
	print "signup here.", request.POST.get('email_address')

	email = request.POST.get('email_address')
	username = request.POST.get('email_address')
	password = request.POST.get('password')

	user = User.objects.filter(email=email)
	if user:
		messages.info(request, 'User already exists')
		return HttpResponseRedirect('/app/signup/')

	user = User.objects.create_user(username, email, password)
	
	user.first_name = request.POST.get('first_name')
	user.last_name = request.POST.get('last_name') 
		
	user.save();

	html = "<html><body>It is saved now in database.</body></html>"
	#return render_to_response('app/user_managment.html', {}, context)
	return HttpResponseRedirect('/app/users')


def user_login(request):
	context = RequestContext(request)

	if request.method == 'POST':

		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/app/')
			else:
				return HttpResponse("Your account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")

	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likely be a HTTP GET.
	else:   
		return render_to_response('app/login.html', {}, context)

@login_required
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)

	# Take the user back to the homepage.
	return HttpResponseRedirect('/app/')

class UserView(ListView):
	template_name = "app/user_managment.html"
	queryset = User.objects.all()

def UserDelete(request, username):
	u = User.objects.get(username = username)
	u.delete()
	#messages.success(request, "The user is deleted")  
	return HttpResponseRedirect('/app/users')

def UserUpdate(request):	
	context = RequestContext(request)

	if request.method == 'POST':
		user = User.objects.get(id=request.POST.get('userid'))
		user.first_name = request.POST.get('fname')
		user.last_name = request.POST.get('lname')
		user.password = request.POST.get('pwd')
		
		user.save();

		return HttpResponseRedirect('/app/users')
	
	else:
		obj = User.objects.get(id=request.GET.get('userid'))
		data = {
			'userid' : request.GET.get('userid'),
			'firstname' : obj.first_name,
			'lastname' : obj.last_name,
		}
		return render_to_response('app/user_edit.html', data, context)


def post_index(request):
	context = RequestContext(request)
	qs = UserPost.objects.all()
	data = {
		'obj_list' : qs 
	}
	return render_to_response('app/users_post.html', data, context)

def post_add(request):
	context = RequestContext(request)
	return render_to_response('app/add_post.html', {}, context)

def user_post_delete_view(request):
	u = UserPost.objects.get(id=request.GET.get('postid'))
	print(u)
	u.delete()
	#messages.success(request, "The user is deleted")  
	return HttpResponseRedirect('/app/users-post')

def post_save(request):	
	context = RequestContext(request)
	print "post ::", request.POST
	if request.method == 'POST':

		if request.POST.get('postid'): #user want to edit
			post_obj = UserPost.objects.get(id=request.POST.get('postid'))
			print "postid::", request.POST.get('postid')
		else: #add new record

			post_obj = UserPost.objects.create()
		
		
		post_obj.title = request.POST.get('title')
		post_obj.category = request.POST.get('category')
		post_obj.description = request.POST.get('description')
		
		post_obj.save();

		return HttpResponseRedirect('/app/users-post')
	
	else:
		obj = UserPost.objects.get(id=request.GET.get('postid'))
		data = {
			'postid' : request.GET.get('postid'),
			'title' : obj.title,
			'category' : obj.category,
			'description' : obj.description,
		}
		return render_to_response('app/update_post.html', data, context)

def emp_index(request):
	context = RequestContext(request)
	qs = EmpData.objects.all()
	data = {
		'obj_list' : qs,
	}
	
	return render_to_response('app/emp_index.html', data, context)

def emp_count(dept):
	noe = EmpData.objects.filter(department=dept).count()
	return noe

def emp_save(request):	
	context = RequestContext(request)
	print "post ::", request.POST
	if request.method == 'POST':

		if request.POST.get('empid'): #user want to edit
			emp_obj = EmpData.objects.get(id=request.POST.get('empid'))
			print "postid::", request.POST.get('postid')
		
		else: #add new record
			emp_obj = EmpData.objects.create()
			
		emp_obj.name        = request.POST.get('name')
		emp_obj.designation = request.POST.get('designation')
		emp_obj.age 		= request.POST.get('age')
		emp_obj.salary 		= request.POST.get('salary')
		emp_obj.department 	= request.POST.get('department')
		emp_obj.projectid 	= request.POST.get('projectid')

		emp_obj.save();

		return HttpResponseRedirect('/app/emp-data')
	
	else:
		obj = EmpData.objects.get(id=request.GET.get('empid'))
		dept_qs = Departments.objects.all()
		project_qs = Project.objects.all()
		desg_qs = Designation.objects.all()
		data = {
			'empid'        : request.GET.get('empid'),
			'name'         : obj.name,
			'designations' : desg_qs,
			'age'          : obj.age,
			'salary'	   : obj.salary,
			'department'   : obj.department,
			'projectid'    : obj.projectid,
			'departments'  : dept_qs,
			'projects' 	   : project_qs,
		}
		return render_to_response('app/add_emp.html', data, context)

def emp_delete(request):
	u = EmpData.objects.get(id=request.GET.get('empid'))
	print(u)
	u.delete()
	#messages.success(request, "The user is deleted")  
	return HttpResponseRedirect('/app/emp-data')


def emp_add(request):
	context = RequestContext(request)
	project_qs = Project.objects.all()
	dept_qs = Departments.objects.all()
	desg_qs = Designation.objects.all()
	data = {
		'projects'    : project_qs,
		'departments' : dept_qs,
		'designations': desg_qs,
	}
	return render_to_response('app/add_emp.html', data, context)


def project_index(request):
	context = RequestContext(request)
	qs = Project.objects.all()
	data = {
		'obj_list' : qs 
	}
	return render_to_response('app/projects.html', data, context)

def project_save(request):	
	context = RequestContext(request)
	#print "post ::", request.POST
	if request.method == 'POST':

		if request.POST.get('projectid'): #user want to edit
			obj = Project.objects.get(id=request.POST.get('projectid'))
		
		else: #add new record

			obj = Project.objects.create()
		
		
		obj.name = request.POST.get('name')
		obj.startdate = request.POST.get('startdate')
		obj.enddate = request.POST.get('enddate')
		
		obj.save();

		return HttpResponseRedirect('/app/projects')
	
	else: # retrive data for edit
		obj = Project.objects.get(id=request.GET.get('projectid'))
		data = {
			'projectid' : request.GET.get('projectid'),
			'name' : obj.name,
			'startdate' : obj.startdate,
			'enddate': obj.enddate,
		}
		return render_to_response('app/add_projects.html', data, context)

def project_add(request):
	context = RequestContext(request)
	return render_to_response('app/add_projects.html', {}, context)

def project_delete(request):
	u = Project.objects.get(id=request.GET.get('projectid'))
	u.delete()

	return HttpResponseRedirect('/app/projects')

def dept_index(request):
	context = RequestContext(request)
	qs = Departments.objects.all()
	
	li = []
	l2 = {}
	for inst in qs:
		l2 = {
			'id': inst.id,
			'name':inst,
			'count':emp_count(inst), 
			'head':inst.head
		}
		li.append(l2)

	print('qwerty: ',li)
	data = {
		'nod' : li,
	}
	return render_to_response('app/departments.html', data, context)

def dept_add(request):
	context = RequestContext(request)
	return render_to_response('app/add_dept.html', {}, context)

def dept_save(request):	
	context = RequestContext(request)
	#print "post ::", request.POST
	if request.method == 'POST':

		if request.POST.get('deptid'): #user want to edit
			obj = Departments.objects.get(id=request.POST.get('deptid'))
		
		else: #add new record

			obj = Departments.objects.create()
		
		
		obj.name = request.POST.get('name')
		obj.head = request.POST.get('head')
		
		obj.save();

		return HttpResponseRedirect('/app/departments')
	
	else: # retrive data for edit
		obj = Departments.objects.get(id=request.GET.get('deptid'))
		data = {
			'deptid' : request.GET.get('deptid'),
			'name' : obj.name,
			'head' : obj.head,
		}
		return render_to_response('app/add_dept.html', data, context)

def dept_delete(request):
	u = Departments.objects.get(id=request.GET.get('deptid'))

	u.delete()

	return HttpResponseRedirect('/app/departments')


def desg_add(request):
	context = RequestContext(request)
	return render_to_response('app/add_desg.html', {}, context)

def desg_index(request):
	context = RequestContext(request)
	qs = Designation.objects.all()
	data = {
		'designations' : qs 
	}
	return render_to_response('app/designations.html', data, context)

def desg_save(request):	
	context = RequestContext(request)
	#print "post ::", request.POST
	if request.method == 'POST':

		if request.POST.get('desgid'): #user want to edit
			obj = Designation.objects.get(id=request.POST.get('desgid'))
		
		else: #add new record

			obj = Designation.objects.create()
		
		
		obj.title = request.POST.get('title')
		
		obj.save();

		return HttpResponseRedirect('/app/designations')
	
	else: # retrive data for edit
		obj = Designation.objects.get(id=request.GET.get('desgid'))
		data = {
			'desgid' : request.GET.get('desgid'),
			'title' : obj.title,
		}
		return render_to_response('app/add_desg.html', data, context)

def desg_delete(request):
	u = Designation.objects.get(id=request.GET.get('desgid'))

	u.delete()

	return HttpResponseRedirect('/app/designations')


