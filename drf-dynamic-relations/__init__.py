"""
Mixin to dynamically eagger load
"""
class DynamicRelationMixin(object):
    """
    """
    def get_queryset(self):
        """
        """
        query_in_fields = self.request.query_params.get('fields')
        if query_in_fields is not None:
            quern_fields = query_in_fields.split(',')

            from django.db.models import ForeignKey, ManyToManyRel, ManyToOneRel

            model_meta = self.queryset.model._meta
            relationables = []
            for field in quern_fields:
                model_field = model_meta.get_field(field)
                if isinstance(model_field, (ForeignKey,
                                            ManyToManyRel,
                                            ManyToOneRel)):
                    relationables.append(field)
            if relationables:
                self.queryset = self.queryset.prefetch_related(*relationables)

        return super(DynamicRelationMixin, self).get_queryset()

