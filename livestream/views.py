from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import SingleObjectMixin
from django.views import generic, View
from rest_framework.response import Response
from rest_framework import status, viewsets, renderers
from rest_framework.renderers import TemplateHTMLRenderer

from .serializers import *
from .models import Appeal

from aLive.settings import OPENTOK_API, OPENTOK_SECRET

from opentok import OpenTok, MediaModes

API_KEY = OPENTOK_API
API_SECRET = OPENTOK_SECRET
opentok = OpenTok(API_KEY, API_SECRET)


# User can create OpenTok Session
# What if ako ning himuon ug read only
# then mag create ko ug CreateSessionView(CreateAPIView) ?? HUH ?? HUUUH??
class AppealViewSet(SingleObjectMixin, viewsets.ModelViewSet):
    queryset = Appeal.objects.all()
    serializer_class = AppealSerializer
    context = {}

    # def get_context_data(self, *args, **kwargs):
    #     self.context = {
    #         'API_KEY': API_KEY,
    #         'SESSION_ID': '',
    #         'TOKEN': token,
    #     }
    #     return context

    def create(self, request, *args, **kwargs):

        session = opentok.create_session(media_mode=MediaModes.routed)
        req = request.data
        if session:
            new_session = Appeal(request_title=req['request_title'],
                                 session_id=session.session_id,
                                 owner=request.user,
                                 helper=None,
                                 detail=req['detail'],)
            new_session.save()
            return Response({'return': 'Successfully created new request'},
                            status=status.HTTP_201_CREATED)

        return Response({'return': 'Failed to create request'})

    def retrieve(self, request, *args, **kwargs):
        '''
        retrieve method gets called when a user accesses a unique session
        user will be given a token to connect to this session
        '''
        # get current user
        print('i get retrieved')
        user = request.user
        print(user)
        # get current session
        appeal = self.get_object()
        print(appeal)
        # check if session owner ang nag generate sa token
        # or check if puno na ang session (max: 2 publishers)
        # generate token for current user (default: publisher) valid for 24h
        # UMIMPLEMENTED PA ANG CHECKING HAP
        token = opentok.generate_token(appeal.session_id)
        # check if token is created successfully
        print(token)
        self.context = {
            'API_KEY': OPENTOK_API,
            'SESSION_ID': appeal.session_id,
            'TOKEN': token,
        }
        print(self.context)
        # serializer = self.get_serializer(session)
        return render(request, 'livestream/stream.html', self.context)
        # return Response(serializer.data,
        #                 template_name='livestream/stream.html')


class AppealDetailView(generic.DetailView):
    model = Appeal
    template_name = 'livestream/stream.html'

    context = {}

    def get(self, request, *args, **kwargs):
        print("i get rendered")

        user = request.user
        print(user)
        # get current session
        appeal = self.get_object()
        print(appeal)
        # check if session owner ang nag generate sa token
        # or check if puno na ang session (max: 2 publishers)
        # generate token for current user (default: publisher) valid for 24h
        # UMIMPLEMENTED PA ANG CHECKING HAP
        token = opentok.generate_token(appeal.session_id)
        # check if token is created successfully
        print(token)
        self.context = {
            'API_KEY': OPENTOK_API,
            'SESSION_ID': appeal.session_id,
            'TOKEN': token,
        }
        print(self.context)

        return self.render_to_response(self.context)


# UserViewSet



# class ClientTokenViewSet(viewsets.ModelViewSet):
#     '''
#         To change:
#             Tokens should not be stored or reused
#     '''
#     queryset = ClientToken.objects.all()
#     serializer_class = ClientTokenSerializer

#     def create(self, request):
#         ret = {'return': 'token creation failed'}
#         req = request.data
#         # get session id from db
#         this_session = Appeal.objects.get(id=req['session'])
#         # generate token
#         token = opentok.generate_token(this_session.session_id)
#         # get user
#         user = User.objects.get(id=req['user'])
#         new_token = ClientToken(token_id=token,
#                                 # fixed wrong parameter thingy
#                                 session=this_session,
#                                 user=user)
#         # check if new token was successfully created
#         # and user does not have existing token
#         print(ClientTokenSerializer(new_token).data)
#         if new_token:
#             print(new_token)
#             # Value error here
#             new_token.save()
#             # VALUE ERROR SOLVED
#             ret = ClientTokenSerializer(new_token).data

#         return Response(ret)


class IndexView(generic.ListView):
    template_name = 'livestream/index.html'
    context_object_name = 'session_list'
    queryset = Appeal.objects.all()
