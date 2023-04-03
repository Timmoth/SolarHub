'use strict';
//import InfluxDB client, this is possible thanks to the layer we created
const { InfluxDB, Point, } = require('@influxdata/influxdb-client')
//grab environment variables
const org = process.env.org
const bucket = process.env.bucket
const token = process.env.token;
const url = process.env.url

module.exports.power = async (event, context, callback) => {

  var body = JSON.parse(event.body)

  const writeApi = await new InfluxDB({ url, token }).getWriteApi(org, bucket);

  const dataPoint = new Point('power')
    .tag('deviceId', body['deviceId'])
    .floatField('loadPower', body['loadPower'])
    .floatField('solarPower', body['solarPower'])
    .floatField('solarVoltage', body['solarVoltage'])
    .floatField('solarCurrent', body['solarCurrent'])


  await writeApi.writePoint(dataPoint)

  await writeApi.close().then(() => {
    console.log('WRITE FINISHED')
  })

  const response = {
    statusCode: 200,
    body: JSON.stringify('Write successful'),
  };

  callback(null, response);
};
