from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.core.fields import RichTextField, StreamField

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel


class HomePage(Page):

    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def __str__(self):
        return self.title


class AboutPage(Page):

    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def __str__(self):
        return self.title


### PEOPLE ###

class PeopleIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only active member, ordered by newest
        context = super().get_context(request)
        peoplepages = self.get_children().live().order_by('-first_published_at')
        context['peoplepages'] = peoplepages
        return context


class PeoplePage(Page):

    name = models.CharField(max_length=60, blank=True)
    description = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('description', classname="full"),
        InlinePanel('people_images', label="People images"),
    ]

    def __str__(self):
        return self.title

    def main_image(self):
        people_images_item = self.people_images.first()
        if people_images_item:
            return people_images_item.image
        else:
            return None


class PeoplePageGalleryImage(Orderable):
    page = ParentalKey(PeoplePage, on_delete=models.CASCADE, related_name='people_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


######

class EventPage(Page):

    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def __str__(self):
        return self.title


class ShowsPage(Page):

    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def __str__(self):
        return self.title


class ContactUsPage(Page):

    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def __str__(self):
        return self.title
