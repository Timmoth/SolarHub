"use strict";
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";

//import InfluxDB client, this is possible thanks to the layer we created
const { InfluxDB, Point } = require("@influxdata/influxdb-client");
//grab environment variables
const org = process.env.org;
const bucket = process.env.bucket;
const token = process.env.token;
const url = process.env.url;

export const power = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  var body = JSON.parse(event.body);

  const writeApi = await new InfluxDB({ url, token }).getWriteApi(org, bucket);

  const dataPoint = new Point("power")
    .tag("deviceId", body["deviceId"])
    .floatField("loadPower", body["loadPower"])
    .floatField("loadCurrent", body["loadCurrent"])
    .floatField("solarPower", body["solarPower"])
    .floatField("solarCurrent", body["solarCurrent"])
    .floatField("solarVoltage", body["solarVoltage"]);

  await writeApi.writePoint(dataPoint);

  await writeApi.close().then(() => {
    console.log("WRITE FINISHED");
  });

  return {
    statusCode: 200,
    body: JSON.stringify("Write successful"),
  };
};
