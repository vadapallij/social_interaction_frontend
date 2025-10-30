# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccelerometerData(models.Model):
    id = models.BigAutoField(primary_key=True)
    family = models.ForeignKey('Families', models.DO_NOTHING, to_field='family_id')
    device_mac = models.ForeignKey('Devices', models.DO_NOTHING, db_column='device_mac')
    sample_at_ms = models.BigIntegerField()
    sample_at_source = models.CharField(max_length=64, blank=True, null=True)
    event_seq = models.BigIntegerField(blank=True, null=True)
    acvl = models.FloatField(blank=True, null=True)
    xyz_count = models.IntegerField(blank=True, null=True)
    ref_station_id = models.CharField(max_length=64, blank=True, null=True)
    ref_scanned_at_ms = models.BigIntegerField(blank=True, null=True)
    time_label = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'accelerometer_data'
        unique_together = (('family', 'device_mac', 'sample_at_ms'),)


class Devices(models.Model):
    device_mac = models.CharField(primary_key=True, max_length=64)
    family = models.ForeignKey('Families', models.DO_NOTHING, to_field='family_id')
    first_seen_ms = models.BigIntegerField(blank=True, null=True)
    last_seen_ms = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'devices'


class Families(models.Model):
    id = models.BigAutoField(primary_key=True)
    family_id = models.CharField(unique=True, max_length=64)

    class Meta:
        managed = False
        db_table = 'families'


class MotionData(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at_ms = models.BigIntegerField(blank=True, null=True)
    family = models.ForeignKey(Families, models.DO_NOTHING, to_field='family_id')
    device_mac = models.ForeignKey(Devices, models.DO_NOTHING, db_column='device_mac')
    event_seq = models.BigIntegerField(blank=True, null=True)
    time_label = models.CharField(max_length=64, blank=True, null=True)
    motion_data_total = models.IntegerField(blank=True, null=True)
    station_id = models.CharField(max_length=64, blank=True, null=True)
    room_type = models.IntegerField(blank=True, null=True)
    rssi = models.IntegerField(blank=True, null=True)
    scanned_at_ms = models.BigIntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'motion_data'
        unique_together = (('family', 'device_mac', 'scanned_at_ms'),)


class PedometerData(models.Model):
    id = models.BigAutoField(primary_key=True)
    family = models.ForeignKey(Families, models.DO_NOTHING, to_field='family_id')
    device_mac = models.ForeignKey(Devices, models.DO_NOTHING, db_column='device_mac')
    sample_at_ms = models.BigIntegerField()
    t_mark_day = models.CharField(max_length=16, blank=True, null=True)
    t_mark_md = models.CharField(max_length=16, blank=True, null=True)
    pedo_d0 = models.IntegerField(blank=True, null=True)
    pedo_d_1 = models.IntegerField(blank=True, null=True)
    pedo_d_2 = models.IntegerField(blank=True, null=True)
    sender_id = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pedometer_data'
        unique_together = (('family', 'device_mac', 'sample_at_ms'),)


class ProximityData(models.Model):
    id = models.BigAutoField(primary_key=True)
    family = models.ForeignKey(Families, models.DO_NOTHING, to_field='family_id')
    device_mac = models.ForeignKey(Devices, models.DO_NOTHING, db_column='device_mac')
    sample_at_ms = models.BigIntegerField()
    sample_at_source = models.CharField(max_length=64, blank=True, null=True)
    event_seq = models.BigIntegerField(blank=True, null=True)
    seq_diff = models.BigIntegerField(blank=True, null=True)
    acvl = models.FloatField(blank=True, null=True)
    cvl_increment = models.FloatField(blank=True, null=True)
    xyz_count = models.IntegerField(blank=True, null=True)
    ref_station_id = models.CharField(max_length=64, blank=True, null=True)
    ref_scanned_at_ms = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'proximity_data'
        unique_together = (('family', 'device_mac', 'sample_at_ms'),)


class RtsStationRssi(models.Model):
    id = models.BigAutoField(primary_key=True)
    packet = models.ForeignKey(ProximityData, models.DO_NOTHING)
    station_alias = models.CharField(max_length=64)
    station_mac = models.CharField(max_length=64, blank=True, null=True)
    rssi = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rts_station_rssi'
        unique_together = (('packet', 'station_alias'),)


class Stations(models.Model):
    station_id = models.CharField(primary_key=True, max_length=64)
    station_name = models.CharField(max_length=128, blank=True, null=True)
    room_type = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stations'


class XyzCoordinates(models.Model):
    id = models.BigAutoField(primary_key=True)
    packet = models.ForeignKey(AccelerometerData, models.DO_NOTHING)
    point_idx = models.IntegerField()
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'xyz_coordinates'
        unique_together = (('packet', 'point_idx'),)
