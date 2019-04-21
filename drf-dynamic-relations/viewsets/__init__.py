"""
For to change the lazy load to eager load while using the dynamic field
in viewsets of django restframework
"""


class DynamicRelationsMixin(object):
    """
    A viewsets mixin that must be used with the restframework viewsets.
    """

    def get_queryset(self):
        """
        Filters the fields according to the `fields` in query parameter.
        it will be improved performance using `prefetch_related`
        """
        query_in_fields = self.request.query_params.get('fields')
        if query_in_fields is not None:
            quern_fields = set(query_in_fields.split(','))

            model_meta = self.queryset.model._meta
            relationables = []
            for field in quern_fields:
                model_field = model_meta.get_field(field)
                if type(model_field).__name__ in ('ForeignKey',
                                                  'ManyToManyRel',
                                                  'ManyToOneRel'):
                    relationables.append(field)
            if relationables:
                self.queryset = self.queryset.prefetch_related(*relationables)

        return super(DynamicRelationsMixin, self).get_queryset()
