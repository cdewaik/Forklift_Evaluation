/**
 * Forklift Operator Evaluation — Apps Script backend.
 *
 * Handles submissions from index.html two ways:
 *   1. Served directly by this project (doGet) — the page calls
 *      submitEvaluation() via google.script.run.
 *   2. Hosted elsewhere (e.g. GitHub Pages) and posting to this project's
 *      deployed Web App URL (doPost) via a hidden-iframe form submit.
 * Both paths append a row to the same Google Sheet.
 *
 * Order here must match the SECTIONS/items order in index.html.
 */

const SHEET_NAME = 'Responses';

const QUESTIONS = [
  ['operatorName', 'Operator being evaluated, first and last name'],
  ['evalDate', "Today's date"],

  ['q1', 'Square up on the center of the load.'],
  ['q2', 'Level the forks; then slowly drive forward until the load contacts the carriage.'],
  ['q3', 'Lift the load carefully and smoothly until it is clear.'],
  ['q4', 'Tilt the mast back slightly to stabilize the load.'],
  ['q5', 'Look over both shoulders.'],

  ['q6', 'After out and stopped, lower the load to travel height.'],
  ['q7', 'Do not raise or lower the load and forks while traveling.'],
  ['q8', 'Maintain a safe speed.'],
  ['q9', 'Observe all traffic rules, warning signs, floor load limits and overhead clearances.'],
  ['q10', 'Keep arms and legs inside the forklift.'],
  ['q11', 'Follow other vehicles at safe distance.'],
  ['q12', 'Slow down when cornering.'],
  ['q13', 'Use the horn to alert others.'],
  ['q14', 'Travel with the load facing uphill while on a ramp or incline.'],

  ['q15', 'Stop smoothly.'],
  ['q16', 'Make sure there is sufficient clearance for the load.'],
  ['q17', 'Clear personnel from the area near the load.'],
  ['q18', 'Square up to the location; then stop about 1 foot away.'],
  ['q19', 'Raise the load to placement level.'],
  ['q20', 'Move slowly forward.'],
  ['q21', 'If the load is on a pallet, lower it into position and lower the forks further.'],
  ['q22', 'Look over both shoulders before backing out.'],
  ['q23', 'Back straight out until the forks have cleared.'],

  ['q24', 'Lower the forks to traveling position.'],
  ['q25', 'Fully lower the forks.'],
  ['q26', 'Neutralize the controls.'],
  ['q27', 'Set the brakes.'],
  ['q28', 'Turn off the power.'],
  ['q29', 'If parked on an incline, block the wheels.'],
  ['q30', 'Park only in authorized areas.'],

  ['q31', 'Engine off.'],
  ['q32', 'Fire extinguisher nearby.'],
  ['q33', 'Proper personal protective equipment worn.'],
  ['q34', 'Safe fueling and battery recharging procedures followed.'],
  ['q35', 'Spills cleaned up immediately.'],

  ['qualifiedEquipment', 'Qualified equipment'],
  ['evaluatorName', 'Evaluator first and last name'],
];

function doGet(e) {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Forklift Operator Evaluation')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function doPost(e) {
  const data = (e && e.parameter) ? e.parameter : {};
  writeRow_(data);
  return ContentService.createTextOutput('OK');
}

function submitEvaluation(data) {
  writeRow_(data || {});
  return { ok: true };
}

function writeRow_(data) {
  const sheet = getSheet_();
  const row = [new Date()].concat(QUESTIONS.map(([key]) => data[key] || ''));
  sheet.appendRow(row);
}

function getSheet_() {
  const props = PropertiesService.getScriptProperties();
  const existingId = props.getProperty('SPREADSHEET_ID');
  const ss = existingId
    ? SpreadsheetApp.openById(existingId)
    : SpreadsheetApp.create('Forklift Operator Evaluations');
  if (!existingId) props.setProperty('SPREADSHEET_ID', ss.getId());

  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow(['Timestamp'].concat(QUESTIONS.map(([, label]) => label)));
    sheet.setFrozenRows(1);
  }
  return sheet;
}
