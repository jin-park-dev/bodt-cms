from django.db import models
from django.utils import timezone

from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

# Create your models here.


### News ###

class NewsIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    subpage_types = ['NewsPage']

    def get_context(self, request):
        # Update context to include only active member, ordered by newest
        context = super().get_context(request)
        newspages = self.get_children().live().order_by('-first_published_at')
        context['newspages'] = newspages
        return context


class NewsPage(Page):

    date = models.DateField("Post date")
    intro = models.CharField(max_length=250, blank=True)
    body = RichTextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('news_images', label="News images"),
    ]

    def __str__(self):
        return self.title

    def main_image(self):
        news_images_item = self.news_images.first()
        if news_images_item:
            return news_images_item.image
        else:
            return None


class NewsPageGalleryImage(Orderable):
    page = ParentalKey(NewsPage, on_delete=models.CASCADE, related_name='news_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]