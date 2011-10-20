# -*- coding: utf-8 -*-
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Avg
from models import FeedbackMember, FeedbackSet
from gp_utils.common.models import Member
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from export_data import export_graph

def index(request):
    if request.user.is_authenticated():
        member = Member.objects.get(user_ptr=request.user)
    else:
        return HttpResponseRedirect(reverse('multisource_feedback.views.login_user'))    
    return render_to_response("./index.html", {'user': member})
    
def evaluate_choose_member(request):
    if request.user.is_authenticated():
        member = Member.objects.get(user_ptr=request.user)
    else:
        return HttpResponseRedirect(reverse('multisource_feedback.views.login_user'))
    member_list = Member.objects.filter(board=member.board).exclude(pk=member.id)
    if member.is_in_board_of_directors:
        director_list = Member.objects.filter(is_in_board_of_directors=True).exclude(pk=member.id)
    else:
        director_list = None
    return render_to_response("./evaluate_choose_member.html", {'user': member,
                                                                'member_list': member_list,
                                                                'director_list': director_list,
                                                                'messages': messages.get_messages(request) } )

def evaluate_member(request, member_id):
    if request.user.is_authenticated():
        evaluator = Member.objects.get(user_ptr=request.user)
    else:
        return HttpResponseRedirect(reverse('multisource_feedback.views.login_user'))
    evaluee = get_object_or_404(Member, pk=member_id)
    return render_to_response("./evaluate_member.html", {'evaluator':evaluator,
                                                         'evaluee': evaluee,
                                                         'criteria': FeedbackMember.CRITERIA },
                                                        context_instance=RequestContext(request))
def submit_feedback(request, member_id):
    if request.user.is_authenticated():
        evaluator = Member.objects.get(user_ptr=request.user)
    else:
        return HttpResponseRedirect(reverse('multisource_feedback.views.login_user'))
    evaluee = get_object_or_404(Member, pk=member_id)
    
    try:
        superset = FeedbackSet.objects.latest('date')
        if superset.finished:
            s = 'A avaliação 360 dessa gestão já foi finalizada'
            messages.add_message(request, messages.ERROR, s)
            return HttpResponseRedirect(reverse('multisource_feedback.views.evaluate_choose_member'))
    except FeedbackSet.DoesNotExist:
        s = 'A avaliação 360 dessa gestão ainda não foi iniciada'
        messages.add_message(request, messages.ERROR, s)
        return HttpResponseRedirect(reverse('multisource_feedback.views.evaluate_choose_member'))

    try:
        FeedbackMember.objects.get(evaluator=evaluator, evaluee=evaluee, superset=superset)
        
        s = 'Você já avaliou este membro nesta gestão'
        messages.add_message(request, messages.ERROR, s)
        return HttpResponseRedirect(reverse('multisource_feedback.views.evaluate_choose_member'))
    except FeedbackMember.DoesNotExist:
        # If it is not already in the system, create feedback for this member pair in this FeedbackSet
        feedback_set = FeedbackSet.objects.latest('date')
        f = FeedbackMember(evaluator=evaluator, evaluee=evaluee, superset=feedback_set)
        try:
            for criterion in FeedbackMember.CRITERIA:
                setattr(f, criterion.name, request.POST[criterion.name])
            f.save()
            s = 'Avaliação realizada com sucesso'
            messages.add_message(request, messages.SUCCESS, s)
            return HttpResponseRedirect(reverse('multisource_feedback.views.evaluate_choose_member'))
        except KeyError:
            s = 'Todos os campos são obrigatórios'
            messages.add_message(request, messages.ERROR, s)
            return HttpResponseRedirect(reverse('multisource_feedback.views.evaluate_member', args=(member_id,)))

def choose_set(request):
    if request.user.is_authenticated():
        member = Member.objects.get(user_ptr=request.user)
    else:
        return HttpResponseRedirect(reverse('multisource_feedback.views.login_user'))
    feedback_sets = FeedbackSet.objects.all()[:5]
    return render_to_response("./choose_set.html", {'sets': feedback_sets },
                                                   context_instance=RequestContext(request))

def view_set(request, set_id):
    if request.user.is_authenticated():
        member = Member.objects.get(user_ptr=request.user)
    else:
        return HttpResponseRedirect(reverse('multisource_feedback.views.login_user'))
    
    feedback_set = get_object_or_404(FeedbackSet, pk=set_id)
    if member.has_perm('multisource_feedback.view_other_feedbacks'):
        members = Member.objects.order_by('board__id')
        return render_to_response("./detail_all.html", {'set': feedback_set,
                                                        'members': members },
                                  context_instance=RequestContext(request))
    else:
        '''
        criteria = FeedbackMember.CRITERIA
        feedbacks = FeedbackMember.objects.filter(evaluee=member, superset=feedback_set)
        feedbacks_board = FeedbackMember.objects.filter(evaluee__board=member.board, superset=feedback_set)
        for criterion in criteria:
            criterion.average =  feedbacks.aggregate(avg=Avg(criterion.name))['avg']
            criterion.average_board =  feedbacks_board.aggregate(avg=Avg(criterion.name))['avg']
            criterion.average_all =  FeedbackMember.objects.aggregate(avg=Avg(criterion.name))['avg']
        
        return render_to_response("./detail_self.html", {'member': member,
                                                         'criteria': criteria},
                                  context_instance=RequestContext(request))
        '''
        s = 'Você não tem permissão para ver esta página'
        messages.add_message(request, messages.ERROR, s)        
        return HttpResponseRedirect(reverse('multisource_feedback.views.login_user'))

def view_one(request, set_id, member_id):
    if request.user.is_authenticated():
        member = Member.objects.get(user_ptr=request.user)
    else:
        return HttpResponseRedirect(reverse('multisource_feedback.views.login_user'))
        
    if not member.has_perm('multisource_feedback.view_other_feedbacks'):
        s = 'Você não tem permissão para ver esta página'
        messages.add_message(request, messages.ERROR, s)        
        return HttpResponseRedirect(reverse('multisource_feedback.views.index'))
    else:
        feedback_set = get_object_or_404(FeedbackSet, pk=set_id)
        evaluee = get_object_or_404(Member, user_ptr__id=member_id)
        criteria = FeedbackMember.CRITERIA
        feedbacks = FeedbackMember.objects.filter(evaluee=evaluee, superset=feedback_set)
        feedbacks_board = FeedbackMember.objects.filter(evaluee__board=evaluee.board, superset=feedback_set)
        for criterion in criteria:
            criterion.average =  feedbacks.aggregate(avg=Avg(criterion.name))['avg']
            criterion.average_board =  feedbacks_board.aggregate(avg=Avg(criterion.name))['avg']
            criterion.average_all =  FeedbackMember.objects.aggregate(avg=Avg(criterion.name))['avg']
            
        return render_to_response("./detail_one.html", {'member': evaluee,
                                                         'criteria': criteria},
                                  context_instance=RequestContext(request))

def export_set(request, set_id):
    pass

def export_member(request, set_id, member_id):
    feedback_set = get_object_or_404(FeedbackSet, pk=set_id)
    evaluee = get_object_or_404(Member, user_ptr__id=member_id)
    criteria = FeedbackMember.CRITERIA
    feedbacks = FeedbackMember.objects.filter(evaluee=evaluee, superset=feedback_set)
    feedbacks_board = FeedbackMember.objects.filter(evaluee__board=evaluee.board, superset=feedback_set)
    for criterion in criteria:
        criterion.average =  feedbacks.aggregate(avg=Avg(criterion.name))['avg']
        criterion.average_board =  feedbacks_board.aggregate(avg=Avg(criterion.name))['avg']
        criterion.average_all =  FeedbackMember.objects.aggregate(avg=Avg(criterion.name))['avg']

    fig = export_graph.export_polargraph(criteria, evaluee)
    canvas=FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect(reverse('multisource_feedback.views.login_user'))
    else:
        return HttpResponseRedirect(reverse('multisource_feedback.views.index'))

def login_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('multisource_feedback.views.index'))
    return render_to_response("./login.html", context_instance=RequestContext(request))

def submit_login(request):
    username = request.POST['login']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('multisource_feedback.views.index'))
        else:
            s = 'Login inválido'
            messages.add_message(request, messages.ERROR, s)        
            return HttpResponseRedirect(reverse('multisource_feedback.views.login_user'))
    else:
        s = 'Login inválido'
        messages.add_message(request, messages.ERROR, s)        
        return HttpResponseRedirect(reverse('multisource_feedback.views.login_user'))
