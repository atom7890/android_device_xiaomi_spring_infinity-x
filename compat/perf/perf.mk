# Required performance framework jars, JNI libraries and binder service only.
# Keep the shared vendor/qcom/common Blueprint pruned to avoid namespace overlap.
PRODUCT_BOOT_JARS += QPerformance UxPerformance
PRODUCT_PACKAGES += \
    QPerformance \
    QXPerformance \
    UxPerformance \
    libqti_performance \
    libqti-iopd-client_system \
    libqti-perfd-client_system \
    vendor.qti.hardware.iop@2.0 \
    spring_perf2_ndk_system \
    perfservice

PRODUCT_COPY_FILES += \
    vendor/qcom/common/system/perf/proprietary/system/etc/permissions/com.qualcomm.qti.Performance.xml:$(TARGET_COPY_OUT_SYSTEM)/etc/permissions/com.qualcomm.qti.Performance.xml \
    vendor/qcom/common/system/perf/proprietary/system/etc/permissions/com.qualcomm.qti.UxPerformance.xml:$(TARGET_COPY_OUT_SYSTEM)/etc/permissions/com.qualcomm.qti.UxPerformance.xml \
    vendor/qcom/common/system/perf/proprietary/system_ext/etc/init/perfservice.rc:$(TARGET_COPY_OUT_SYSTEM_EXT)/etc/init/perfservice.rc \
    vendor/qcom/common/system/perf/proprietary/system_ext/etc/seccomp_policy/perfservice.policy:$(TARGET_COPY_OUT_SYSTEM_EXT)/etc/seccomp_policy/perfservice.policy
