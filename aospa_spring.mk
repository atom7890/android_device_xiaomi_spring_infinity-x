#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#
# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Platform required during product configuration
TARGET_BOARD_PLATFORM := blair
TARGET_KERNEL_VERSION := 6.1
TARGET_USES_KERNEL_PLATFORM := false

# Use the UFS BSG interface with the prebuilt 6.1 kernel headers.
$(call soong_config_set,ufsbsg,ufsframework,bsg)

# Inherit some common PenguinOS / AOSPA stuff.
$(call inherit-product, vendor/aospa/target/product/aospa-target.mk)

# Inherit from spring device
$(call inherit-product, device/xiaomi/spring/device.mk)

# Device identifiers
PRODUCT_DEVICE := spring
PRODUCT_NAME := aospa_spring
PRODUCT_BRAND := Redmi
PRODUCT_MODEL := 25057RN09G
PRODUCT_MANUFACTURER := Xiaomi

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="spring_global-user 16 BP2A.250605.031.A3 16OS3.1.260915.200026040.QCPEGL.S release-keys" \
    BuildFingerprint=Xiaomi/spring_global/spring:16/BP2A.250605.031.A3/16OS3.1.260915.200026040.QCPEGL.S:user/release-keys \
    DeviceName=spring \
    DeviceProduct=spring_global

# GMS
PRODUCT_GMS_CLIENTID_BASE := android-xiaomi

# Keep legacy Make modules except the Wi-Fi modules already built by Soong.
PRODUCT_IGNORE_ALL_ANDROIDMK := true
PRODUCT_ANDROIDMK_ALLOWLIST_FILE := device/xiaomi/spring/androidmk-allowlist.mk
