from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Task(models.Model):
    title = models.CharField(max_length=255, default="Untitled Task")
    type = models.CharField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=10, default="00:00")
    date = models.DateField(default=timezone.now)
    tasks = models.JSONField(default=list, blank=True)

    color = models.CharField(max_length=20, default="#FFFFFF")
    cardColor = models.CharField(max_length=20, default="4294967295")  # white
    titleColor = models.CharField(max_length=20, default="4278190080")  # black

    audio_file = models.FileField(upload_to="voices/", null=True, blank=True)

    # ── System fields ─────────────────────────────
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title or "task")
            slug = base_slug
            counter = 1
            while Task.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or "Unnamed Task"
