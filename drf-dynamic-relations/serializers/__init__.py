"""
"""
import warnings

from django.conf import settings


class DynamicFieldsMixin(object):
    def __init__(self, *args, **kwargs):
        self.Meta.fields = tuple(set(self.Meta.fields +
                                     self.Meta.includible_fields))
        super(DynamicFieldsMixin, self).__init__(*args, **kwargs)

    @property
    def fields(self):
        """
        Filters the fields according to the `include` query parameter.
        A blank `include` parameter (?include) will remove all fields. Not
        passing `fields` will pass all fields individual fields are comma
        separated (?include=id,name,url,email).
        """

        fields = super(DynamicFieldsMixin, self).fields

        if not hasattr(self, '_context'):
            # We are being called before a request cycle
            return fields

        # Only filter if this is the root serializer, or if the parent is the
        # root serializer with many=True
        is_root = self.root == self
        parent_is_list_root = self.parent == self.root and getattr(self.parent,
                                                                   'many',
                                                                   False)
        if not (is_root or parent_is_list_root):
            return fields

        try:
            request = self.context['request']
        except KeyError:
            conf = getattr(settings, 'DRF_DYNAMIC_FIELDS', {})
            if not conf.get('SUPPRESS_CONTEXT_WARNING', False) is True:
                warnings.warn('Context does not have access to request. '
                              'See README for more information.')
            return fields

        # NOTE: drf test framework builds a request object where the query
        # parameters are found under the GET attribute.
        params = getattr(
            request, 'query_params', getattr(request, 'GET', None)
        )
        if params is None:
            warnings.warn('Request object does not contain query paramters')

        try:
            omit_fields = params.get('omit', None).split(',')
        except AttributeError:
            omit_fields = []

        try:
            filter_fields = params.get('fields', None).split(',')
        except AttributeError:
            filter_fields = None
            try:
                include_fields = params.get('include', None).split(',')
            except AttributeError:
                include_fields = []

        # Drop any fields that are not specified in the `fields` argument.
        existing = set(fields.keys())
        if filter_fields is None:
            # no fields param given, don't filter.
            allowed = existing
        else:
            allowed = set(filter(None, filter_fields))

        # omit fields in the `omit` argument.
        omitted = set(filter(None, omit_fields))

        excluded_fields = set(self.Meta.includible_fields) - set(
            filter_fields if filter_fields is not None else include_fields)

        for field in excluded_fields:
            fields.pop(field, None)

        for field in existing:
            if field not in allowed:
                fields.pop(field, None)
            if field in omitted:
                fields.pop(field, None)

        return fields
