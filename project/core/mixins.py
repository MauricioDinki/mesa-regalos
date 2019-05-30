class RequestFormMixin(object):
    """CBV mixin wich puts the request in the kwargs of a form"""
    def get_form_kwargs(self):
        kwargs = super(RequestFormMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs