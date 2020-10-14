class Device:
    def __init__(self, room):
        self._identifier = self._read("/etc/hostname").strip("\n")
        self._name = room.capitalize()
        self._model = self._read("/sys/firmware/devicetree/base/model").strip("\n")
        self._sw_version = self._os_release()["PRETTY_NAME"]
        self._manufacturer = ""

    def id(self):
        return self._identifier

    def template(self):
        return {
              "identifiers": [
                  self._identifier
              ],
              "name": self._name,
              "model": self._model,
              "sw_version": self._sw_version,
              "manufacturer": self._manufacturer
          }

    def _read(self, filename):
        f = open(filename, "r")
        data = f.read()
        f.close()
        return data

    def _os_release(self):
        release = self._read("/etc/os-release")
        keys = []
        values = []
        for line in release.splitlines:
            kv = line.split("=",1)
            keys.append(kv[0])
            values.append(kv[1].strip('"'))
        return dict(zip(keys, values))
