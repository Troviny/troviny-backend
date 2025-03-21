# Generated by Django 5.1.6 on 2025-03-17 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('profile_picture', models.TextField(blank=True, null=True)),
                ('country', models.TextField(blank=True, null=True)),
                ('city', models.TextField(blank=True, null=True)),
                ('role', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='api_user_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='api_user_permissions_set', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
