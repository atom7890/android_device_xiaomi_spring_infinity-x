/* SPDX-License-Identifier: Apache-2.0 */
#include <aidl/vendor/aospa/power/Feature.h>
#include <android-base/file.h>
#include <android-base/logging.h>
#include <android-base/unique_fd.h>
#include <dirent.h>
#include <fcntl.h>
#include <linux/input.h>
#include <sys/ioctl.h>
#include <unistd.h>

#include <cstring>
#include <memory>
#include <mutex>
#include <string>

namespace aidl::vendor::aospa::power {
namespace {
std::mutex gestureMutex;
bool gesturesEnabled = true;
bool doubleTapEnabled = false;

bool updateTouchscreen(bool enabled) {
    std::unique_ptr<DIR, decltype(&closedir)> inputs(opendir("/dev/input"), closedir);
    if (!inputs) {
        PLOG(ERROR) << "Cannot enumerate touchscreen inputs";
        return false;
    }
    while (dirent* entry = readdir(inputs.get())) {
        if (strncmp(entry->d_name, "event", 5) != 0) continue;
        const std::string path = std::string("/dev/input/") + entry->d_name;
        ::android::base::unique_fd fd(open(path.c_str(), O_RDWR | O_CLOEXEC));
        if (fd.get() < 0) continue;
        char name[80] = {};
        if (ioctl(fd.get(), EVIOCGNAME(sizeof(name) - 1), name) <= 0) continue;
        if (strcmp(name, "fts_ts") != 0 && strcmp(name, "NVTCapacitiveTouchScreen") != 0) {
            continue;
        }
        input_event event{};
        event.type = EV_SYN;
        event.code = SYN_CONFIG;
        event.value = enabled ? 5 : 4;
        if (!::android::base::WriteFully(fd.get(), &event, sizeof(event))) {
            PLOG(ERROR) << "Cannot update touchscreen double-tap mode";
            return false;
        }
        return true;
    }
    LOG(ERROR) << "No supported touchscreen found for double-tap mode";
    return false;
}
}  // namespace

bool setDeviceSpecificFeature(Feature feature, bool enabled) {
    std::lock_guard<std::mutex> lock(gestureMutex);
    switch (feature) {
        case Feature::GESTURES:
            gesturesEnabled = enabled;
            break;
        case Feature::DOUBLE_TAP:
            doubleTapEnabled = enabled;
            break;
        default:
            return false;
    }
    return updateTouchscreen(gesturesEnabled && doubleTapEnabled);
}
}  // namespace aidl::vendor::aospa::power
