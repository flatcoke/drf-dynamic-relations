"""
For to change the lazy load to eager load while using the dynamic field
in viewsets of django restframework
"""
from rest_framework.serializers import FieldDoesNotExist


class DynamicRelationsMixin(object):
    """
    A viewsets mixin that must be used with the restframework viewsets.
    """

    QUERY_KEYS = ['include', 'fields']

    def get_queryset(self):
        """
        Filters the fields according to the `fields` in query parameter.
        it will be improved performance using `prefetch_related`
        """
        query_in_fields = []
        for i in self.QUERY_KEYS:
            try:
                query_in_fields = query_in_fields + \
                                  self.request.query_params.get(i).split(',')
            except AttributeError:
                pass

        if query_in_fields:
            model_meta = self.queryset.model._meta
            relationables = []
            for field in query_in_fields:
                try:
                    model_field = model_meta.get_field(field)
                    if type(model_field).__name__ in ('ForeignKey',
                                                      'ManyToManyRel',
                                                      'ManyToOneRel'):
                        relationables.append(field)
                except FieldDoesNotExist:
                    pass
            if relationables:
                self.queryset = self.queryset.prefetch_related(*relationables)

        return super(DynamicRelationMixin, self).get_queryset()
