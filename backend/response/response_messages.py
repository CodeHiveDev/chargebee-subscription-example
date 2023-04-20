from django.utils.translation import gettext_lazy as _


class ApiResponseMessages:
    def __init__(self):

        self.field_missing = _(u'Invalid request! or fields are missing!'),
        self.signin_success = u"Your account has been created success fully"
        self.email_already_exists = u"A user with that email address already exists."
        self.user_already_exists = u"Username is already exits."
        self.user_email_not_active = u"Your email id not registered."
        self.admin_email_not_active = u"Your email id is not registered with admin credentials."
        self.invalid_credentials = u"Please check your password again."
        self.not_activate = u"Your email id is not activated. Please check your email to activate your account."
        self.activate_account = u"Your account has been activated successfully, please login and check."
        self.already_activate = u"Account is already active."
        self.not_found = u"User details not found."
        self.invalid_email = u"Email id is not valid"
        self.forgetpassword = u"Reset password link has been sent to your email id, please check it."
        self.account_not_fount = u"Account not found."
        self.invalid_email_credentials = u"Invalid request!."
        self.password_reset = u"Your account password has been updated successfully."
        self.password_reset_session_exp = u"Your reset password link has expired."
        self.success = u"Your account logout successfully."
        self.send_email_failure = u"Application failed to send to email."
        self.user_status_change = u"User account status has been updated"
        self.user_status_not_change = u"User account status doesn't update"

        self.product_status = u"product detail has been added successfully."
        self.update_product = u"product detail has been updated successfully."
        self.not_update_product = u"product detail has been not update."
        self.product_delete = u"product detail has been deleted successfully."
        self.product_retrieve = u"product detail has been retrieved successfully."
        self.product_not_found = u"product id not found."
        self.product_empty = u'product detail has been empty'

        self.article_create = u"Article has been created successfully."
        self.article_delete = u'Article has been deleted successfully'
        self.article_not_found = u'Article not found'
        self.article_update = u'Article has been updated successfully.'
        self.image_upload = u'Image has been uploaded successfully'
        self.image_not_upload = u'Failed to upload the image into s3 bucket'

        self.blog_data_add = u'Blog details has been added successfully.'
        self.blog_data_update = u'Blog details has been updated successfully.'
        self.blog_retrieve = u"Blog detail has been retrieved successfully."
        self.blog_not_found = u"Blog id not found."
        self.blog_empty = u"Blog detail has been empty."

        self.contact_status = u"product detail has been added successfully."
