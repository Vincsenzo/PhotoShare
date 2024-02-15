# Generated by Django 4.2.6 on 2024-02-15 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['-uploaded']},
        ),
        migrations.CreateModel(
            name='Galleries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gallery_name', models.CharField(max_length=30, null=True)),
                ('photos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.photo')),
            ],
        ),
    ]
