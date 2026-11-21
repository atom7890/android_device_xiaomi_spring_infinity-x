LOCAL_PATH := $(call my-dir)

ifndef add-radio-file-sha1-checked
define add-radio-file-sha1-checked
  $(eval path := $(LOCAL_PATH)/$(1))
  $(eval sha1 := $(shell sha1sum "$(path)" | cut -d" " -f 1))
  $(if $(filter $(sha1),$(2)),\
    $(call add-radio-file,$(1)),\
    $(error $(path) SHA1 mismatch ($(sha1) != $(2))))
endef
endif

# Preserve Qualcomm component rules.
include $(call all-makefiles-under,device/qcom/common)

# Preserve legacy board setup with only duplicate Soong mountpoint recipes removed.
ifeq ($(call is-board-platform-in-list,$(QCOM_BOARD_PLATFORMS)),true)
ifeq ($(TARGET_FWK_SUPPORTS_FULL_VALUEADDS),true)
include device/xiaomi/spring/AndroidBoardCompat.mk
endif
endif
