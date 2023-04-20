from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from django.shortcuts import redirect
# Create your views here.
from response.api_response import CustomResponse
from response.response_messages import ApiResponseMessages
from django.conf import settings
import chargebee
import json
import stripe
from .models import *
from .serializer import*
import datetime


api_msg_obj = ApiResponseMessages()
chargebee.configure(
    "test_lZjjYibCadW28WhgSvxoSraEySgvpu8E", "fantasytech-test")


# chargebee.configure(
#     "test_cumQCNlPuhCR0dnbFuzbblqJFLErWlyp", "scudtester-test")

# This api was finished


@permission_classes((AllowAny, ))
class PaymentSubscription(APIView):
    def post(self, request):
        user_detail = User.objects.get(id=request.POST.get('user_id'))
        result = chargebee.HostedPage.checkout_new_for_items({
            "subscription_items": [
                {
                    "item_price_id": request.POST.get('item_price_id'),
                    "unit_price": request.POST.get('unit_price'),
                    "quantity": 1,
                    "item_type": "plan",
                    "object": "subscription_item"
                }
            ],
            "redirect_url": "http://localhost:3000/",
            'embed': {
                'hide_coupon_input': True
            },
            "customer": {
                "email": user_detail.email,
                "first_name": user_detail.first_name,
                "last_name": user_detail.last_name,
                "auto_collection": "on",
            }

        })
        return redirect(result.hosted_page.url)


@permission_classes((AllowAny,))
class GetCharbeSubscription(APIView):
    def get(self, request):
        cc = chargebee.Subscription.list({
            "customer_id": "cbdemo_richard"
        })
        list_data = []
        for i in cc:
            data = {}
            data['subscription_id'] = i.subscription.id
            data['currency_code'] = i.subscription.currency_code
            data['billing_period_unit'] = i.subscription.billing_period_unit
            new_item = []
            for j in i.subscription.subscription_items:
                new_data = {}
                new_data['item_price_id'] = j.item_price_id
                new_data['amount'] = j.amount
                new_item.append(new_data)
            data['subscription_items'] = new_item
            data['customer_id'] = i.customer.id
            data['backend_url'] = settings.APP_URL
            if int(new_data['amount']):
                list_data.append(data)
        msg = "Retirive data succuessfully"
        status_code = status.HTTP_200_OK
        resp_json = CustomResponse.data_response(list_data, status_code, msg)
        return Response(resp_json)


@permission_classes((AllowAny, ))
class PaymetWebHook(APIView):
    def post(self, request):
        try:
            # Parse the webhook data
            data = request.data
            # data = json.loads(request.data)
            event_type = data['event_type']
            subscription_id = data['content']['subscription']['id']
            # if event_type == 'subscription_created' or event_type == "payment_succeeded":
            if event_type == 'subscription_created':
                email = data['content']['customer']['email']
                customer_id = data['content']['subscription']['customer_id']
                status = data['content']['subscription']['status']
                item_price_id = data['content']['subscription']['subscription_items'][0]['item_price_id']
                amount = data['content']['subscription']['subscription_items'][0]['amount']
                start_date = data['content']['subscription']['current_term_start']
                try:
                    user_data = User.objects.get(email=email)
                    dt_object = datetime.datetime.fromtimestamp(start_date)
                    date_string = dt_object.strftime("%Y-%m-%d")
                    sub_data = Subscription(
                        user=user_data,
                        subscription=subscription_id,
                        amount=amount,
                        item_price_id=item_price_id,
                        customer_id=customer_id,
                        start_date=date_string,
                        status=status,
                    )
                    sub_data.save()
                except Exception as er:
                    pass
                # Handle the subscription cancelled event
                # You can update your database or send an email notification here
                pass
            return Response(status=200)
        except Exception as er:
            return Response('Invalid request body')


@permission_classes((AllowAny, ))
class LoginView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request):
        """
        This API is used to generate a auth token for login purpose.

        @param request: email and password
        @return: retruns a auth token object along with user data.
        """
        data = request.data
        login_serializer = UserLoginSerializer(data=data)
        print(login_serializer)
        if login_serializer.is_valid():
            email = data['email']
            password = data['password']
            valid_email = User.objects.filter(
                email__iexact=data['email'], status='Active')

            if valid_email:
                check_to_active_email = User.objects.filter(
                    email__iexact=data['email'], is_active=True)

                if check_to_active_email:
                    request_user = login_serializer.authenticate(
                        email=email, password=password)

                    if request_user:
                        try:
                            Token.objects.get(user=request_user).delete()
                        except Exception as er:
                            pass
                        Token.objects.create(user=request_user)
                        new_token = list(Token.objects.filter(
                            user_id=request_user).values("key"))
                        msg = {
                            "token": str(new_token[0]['key']),
                            'user': str(request_user),
                            'user_id': request_user.id,
                            'status': status.HTTP_201_CREATED
                        }
                        return Response(msg, status=status.HTTP_201_CREATED)

                    else:
                        msg = api_msg_obj.invalid_credentials
                        status_code = status.HTTP_400_BAD_REQUEST
            else:
                msg = api_msg_obj.user_email_not_active
                status_code = status.HTTP_400_BAD_REQUEST
        else:
            msg = api_msg_obj.field_missing[0]
            status_code = status.HTTP_401_UNAUTHORIZED

        resp_json = CustomResponse.default_response(msg, status_code)
        return Response(resp_json, status=status_code)


@permission_classes((AllowAny, ))
class SignUpView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        """
        This api create a new user account

        :param request: username, email and password
        :return: returns user creation json reponse
        """
        data = {"username": request.data['email'],
                'email': request.data['email'],
                'first_name': request.data['first_name'],
                'last_name': request.data['last_name'],
                'password': request.data['password']}
        valid_email = User.objects.filter(email__iexact=data['email'])
        if valid_email:
            msg = api_msg_obj.email_already_exists
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            try:
                serializer = UserSerializer(data=data)
                valid = serializer.is_valid(raise_exception=True)
                if valid:
                    user = serializer.save()
                    try:
                        msg = api_msg_obj.signin_success
                        status_code = status.HTTP_201_CREATED
                    except:
                        msg = api_msg_obj.send_email_failure
                        status_code = status.HTTP_408_REQUEST_TIMEOUT
                else:
                    msg = api_msg_obj.field_missing
                    status_code = status.HTTP_400_BAD_REQUEST

            except KeyError:
                msg = api_msg_obj.field_missing[0]
                status_code = status.HTTP_400_BAD_REQUEST

        resp_json = CustomResponse.default_response(msg, status_code)
        return Response(resp_json, status=status_code)
