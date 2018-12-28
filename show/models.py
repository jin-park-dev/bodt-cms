from django.db import models
from django.utils import timezone

from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from embed_video.fields import EmbedVideoField


class ShowIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    subpage_types = ['ShowPage']

    def get_context(self, request):
        # Update context to include only active show, ordered by newest
        context = super().get_context(request)
        showpages = self.get_children().live().order_by('-first_published_at')
        context['showpages'] = showpages
        context['showpage_first'] = showpages[0]
        return context


class ShowPage(Page):

    date = models.DateField("Show Date")
    name = models.CharField(max_length=250, blank=True)
    body = RichTextField(blank=True)
    video = EmbedVideoField()
    timestamp = models.DateTimeField(default=timezone.now)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('title'),
        FieldPanel('body'),
        FieldPanel('video'),
        InlinePanel('show_images', label="Show images"),
    ]

    def __str__(self):
        return self.title

    def main_image(self):
        show_images_item = self.show_images.first()
        if show_images_item:
            return show_images_item.image
        else:
            return None


    def get_context(self, request):
        # Update context to include only active show, ordered by newest
        context = super().get_context(request)
        showpages = Page.objects.get(slug='shows').get_children().live().order_by('-first_published_at')
        context['showpages'] = showpages
        context['showpage_first'] = self
        return context



class ShowPageGalleryImage(Orderable):
    page = ParentalKey(ShowPage, on_delete=models.CASCADE, related_name='show_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
