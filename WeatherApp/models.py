from django.contrib.auth.models import User
from django.db import models
from ordered_model.models import OrderedModel


class Location(OrderedModel):
    """Model definition for Locations (like city or town)"""

    name = models.TextField()
    temperature = models.TextField()
    description = models.TextField()
    icon = models.TextField()

    # a Many-to-One relationship with User Model
    owner = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name="owner")

    class Meta(OrderedModel.Meta):
        # User can not request weather information for same location more than once
        unique_together = (("name", "owner"),)

    def __str__(self):
        return ' '.join(["Location name:", self.name, ", Belongs to:", str(self.owner.username)])

