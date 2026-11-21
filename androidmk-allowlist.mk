# Preserve discovered Makefiles except legacy Wi-Fi and Qualcomm board wrappers.
allowed_androidmk_files += $(filter-out \
    hardware/qcom/wlan/% \
    device/qcom/common/Android.mk,\
    $(file <$(OUT_DIR)/.module_paths/Android.mk.list))
