import "jest";
import axios from "axios";

describe("readings tests", () => {
  it("should return 200", async () => {
    let body = JSON.stringify({
      deviceId: 1,
      loadPower: 2,
      loadCurrent: 3,
      solarPower: 4,
      solarCurrent: 5,
      solarVoltage: 6,
    });
    const { status } = await axios.post(`http://localhost:3000/power`, body);
    expect(status).toEqual(200);
  });
});
