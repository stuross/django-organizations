from django.db import models

from south.modelsinspector import add_introspection_rules


class UniqueCharField(models.CharField):
    """
    Nothing more than a char field with a pre_save method of its own. Useful
    for char fields which should be unique where Null is allowed.
    """

    def __init__(self, *args, **kwargs):
        kwargs.update({"blank": True, "null": True, "unique": True})
        super(UniqueCharField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """Ensure that the value is null, not blank"""
        curr_val = getattr(model_instance, self.attname)
        return curr_val if curr_val is not "" else None


add_introspection_rules([], ["^accounts\.fields\.UniqueCharField"])
