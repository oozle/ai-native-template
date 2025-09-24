#!/usr/bin/env node
import fs from "fs";
import path from "path";

const args = process.argv.slice(2);
const cmd = args[0];

function usage() {
  console.log("Usage: agentapi fees:validate [path]");
}

if (cmd === "fees:validate") {
  const file = args[1] || "providers/demo-openweather/adapter/pricing/apifee.json";
  if (!fs.existsSync(file)) {
    console.error(`File not found: ${file}`);
    process.exit(1);
  }
  const data = JSON.parse(fs.readFileSync(file, "utf-8"));
  const missing = [];
  if (!data.provider) missing.push("provider");
  if (!data.currency) missing.push("currency");
  if (!data.plans || !Array.isArray(data.plans) || data.plans.length === 0) missing.push("plans");
  if (missing.length) {
    console.error("Invalid fee menu: missing " + missing.join(", "));
    process.exit(1);
  }
  console.log(`✅ Fee menu for ${data.provider} looks valid.`);
  process.exit(0);
} else {
  usage();
  process.exit(0);
}
