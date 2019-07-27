from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel

from news.models import NewsPage
from event.models import EventPage
from show.models import ShowPage

from puput.models import BlogPage, EntryPage


class HomePage(Page):

    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    # Event, Other pages to create on Homepage
    subpage_types = ['AboutPage', 'PeopleIndexPage', 'news.NewsIndexPage',
                     'show.ShowIndexPage', 'event.EventIndexPage', 'ContactUsPage',
                     'puput.BlogPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        # print('BlogPage')
        # print(BlogPage)
        # newspages = BlogPage.objects.live().order_by('-first_published_at')[0:3]
        newspages = EntryPage.objects.live().order_by('-date')[0:3]  # Latest 3
        # print('blogpage')
        # print(blogpage)

        # newspages = NewsPage.objects.live().order_by('-first_published_at')[0:3]
        # print(newspages.first().__dict__)
        context['newspages'] = reversed(newspages) # To get order from last to newest (on the right)

        eventpages = EventPage.objects.live().order_by('-first_published_at')[0:3]
        context['eventpages'] = eventpages

        # peoplepages = PeoplePage.objects.live().order_by('-first_published_at')[0:8]
        # peoplepages = PeoplePage.objects.live().order_by('?')[0:8]
        peoplepages = PeoplePage.objects.live().filter(featured=True).order_by('ordering_priority')[0:8]
        context['peoplepages'] = peoplepages

        # Same as news. Take 3 latest and make order from oldest to newest.
        showpages = ShowPage.objects.live().order_by('-first_published_at')[0:3]
        context['showpages'] = reversed(showpages)

        return context

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

    subpage_types = ['PeoplePage']

    def get_context(self, request):
        # Update context to include only active member, ordered by newest
        context = super().get_context(request)
        peoplepages = self.get_children().live().order_by('-first_published_at')
        context['peoplepages'] = peoplepages
        return context


class PeoplePage(Page):

    name = models.CharField(max_length=60, blank=True)
    description = RichTextField()
    featured = models.BooleanField(default=False, help_text='Shows on the homepage')
    past = models.BooleanField(default=False)
    ordering_priority = models.IntegerField(blank=True, null=True, default=5,
                                            # validators=[MaxValueValidator(10), MinValueValidator(1)],
                                            choices=[(i,i) for i in range(1, 11)],
                                            ) # Between 1-10?

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('description', classname="full"),
        InlinePanel('people_images', label="People images"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('featured', classname="col4"),
                FieldPanel('ordering_priority', classname="col4"),
                FieldPanel('past', classname="col4")
            ]),
        ], heading='Helpful Ordering'),
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


### CONTACT US ###
"""
Uses wagtail's built in class to create simple form
"""


class ContactUsFormField(AbstractFormField):

    page = ParentalKey('ContactUsPage', on_delete=models.CASCADE, related_name='form_fields')


class ContactUsPage(AbstractEmailForm):

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]
