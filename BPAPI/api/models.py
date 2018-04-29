from django.db import models
from django.utils import timezone


from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError


def parent_sets_changed(sender, **kwargs):
    if kwargs['instance'].regions.count() > 2:
        raise ValidationError("You can't assign more than two parent sets")


class Player(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    tag = models.CharField(max_length=20)
    main = models.ForeignKey('Character', on_delete=models.PROTECT)

    def __repr__(self):
        return '<Player: {} "{}" {}>'.format(self.first_name, self.tag, self.last_name)


class Character(models.Model):
    name = models.CharField(max_length=20)

    weight = models.IntegerField(null=True)
    air_speed = models.FloatField(null=True)
    walking_speed = models.FloatField(null=True)
    falling_speed = models.FloatField(null=True)
    initial_dash = models.FloatField(null=True)
    dash_frames = models.IntegerField(null=True)
    dash_acceleration = models.FloatField(null=True)
    run_speed = models.FloatField(null=True)
    jump_force = models.FloatField(null=True)
    gravity = models.FloatField(null=True)
    fast_fall_mod = models.FloatField(null=True)
    air_acceleration_base = models.FloatField(null=True)
    air_acceleration_additional = models.FloatField(null=True)
    air_acceleration_max = models.FloatField(null=True)
    air_friciton = models.FloatField(null=True)
    traction = models.FloatField(null=True)

    def __repr__(self):
        return '<Character: {}>'.format(self.name)


class Game(models.Model):
    player_one_character = models.ForeignKey(Character, on_delete=models.PROTECT, related_name='player_one_character')
    player_two_character = models.ForeignKey(Character, on_delete=models.PROTECT, related_name='player_two_character')
    gameTime = models.DurationField()
    set = models.ForeignKey("Set", on_delete=models.CASCADE)


class Set(models.Model):
    player_one = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_one')
    player_two = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_two')
    games = models.ManyToManyField(Game, related_name='games', blank=True)
    date_time = models.DateTimeField(default=timezone.now)
    parents = models.ManyToManyField('self', symmetrical=False, blank=False)

    def __repr__(self):
        return '<Set: {} vs. {} on {}>'.format(player_one, player_two, date_time)


m2m_changed.connect(parent_sets_changed, sender=Set.parents.through)
