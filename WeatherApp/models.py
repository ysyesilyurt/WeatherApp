from django.contrib.auth.models import User
from django.db import models
from ordered_model.models import OrderedModel


class Location(OrderedModel):
    """Model definition for Locations (like city or town)"""

    name = models.TextField()
    temparature = models.TextField()
    description = models.TextField()
    icon = models.TextField()

    # additionalAttribute is like 'Home' or 'Workplace' etc.
    additionalAttribute = models.TextField(blank=True, null=True)

    # a Many-to-One relationship with User Model
    owner = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name="owner")

    class Meta(OrderedModel.Meta):
        # User can not request weather information for same location more than once
        unique_together = (("name", "owner"),)

    def __str__(self):
        if self.additionalAttribute is not None:
            return ' '.join(["Location name:", self.name, ", Additional Attribute:", str(self.additionalAttribute),
                             ", Belongs to:", str(self.owner.username)])
        return ' '.join(["Location name:", self.name, ", Belongs to:", str(self.owner.username)])

