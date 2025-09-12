# todo ______________ v3

# tasks/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Task(models.Model):
    # ── Main fields ──────────────────────────────────────────
    title = models.CharField(
        max_length=200,
        blank=True,  # <-- allows empty title in forms
        null=True,  # <-- allows NULL in DB
        help_text="Short label for the task, e.g. Studying, Meditating",
    )
    content = models.TextField(
        null=True, blank=True, help_text="Detailed description or context of the task"
    )
    type = models.CharField(max_length=100, null=True, blank=True)  # optional category
    time = models.TimeField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    tasks = models.JSONField(default=list, blank=True)

    # ── Voice support ────────────────────────────────────────
    audio_file = models.FileField(
        upload_to="voice_notes/",
        null=True,
        blank=True,
        help_text="Optional audio file if added via voice",
    )
    transcript = models.TextField(
        null=True, blank=True, help_text="AI-generated transcript from audio"
    )

    # ── System fields ────────────────────────────────────────
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
        return self.title
