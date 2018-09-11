from django.db import models
from django.utils import timezone

from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel


class EventIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    subpage_types = ['EventPage']

    def get_context(self, request):
        # Update context to include only active event, ordered by newest
        context = super().get_context(request)
        eventpages = self.get_children().live().order_by('-first_published_at')
        context['eventpages'] = eventpages
        return context


class EventPage(Page):

    date_post = models.DateField("Posting Date")
    date_event = models.CharField("Event date", max_length=250)
    name = models.CharField(max_length=250, blank=True)
    address = models.CharField(max_length=250, blank=True)
    body = RichTextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    content_panels = Page.content_panels + [
        FieldPanel('date_post'),
        FieldPanel('date_event'),
        FieldPanel('name'),
        FieldPanel('address'),
        FieldPanel('body'),
        InlinePanel('event_images', label="Event images"),
    ]

    def __str__(self):
        return self.title

    def main_image(self):
        event_images_item = self.event_images.first()
        if event_images_item:
            return event_images_item.image
        else:
            return None


class EventPageGalleryImage(Orderable):

    page = ParentalKey(EventPage, on_delete=models.CASCADE, related_name='event_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
