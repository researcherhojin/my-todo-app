/**
 * Phase 4 통합 Playwright 스크린샷 캡처
 * Usage: npx playwright test --config=scripts/capture-screenshots.mjs (X)
 * Usage: node scripts/capture-screenshots.mjs (via playwright module)
 */

import { chromium } from "playwright";
import { mkdirSync } from "fs";
import { join } from "path";

const PORT = process.env.PORT || "8001";
const BASE_URL = `http://localhost:${PORT}`;
const SCREENSHOT_DIR = join(process.cwd(), "docs", "screenshots");

mkdirSync(SCREENSHOT_DIR, { recursive: true });

async function screenshot(page, name) {
  const path = join(SCREENSHOT_DIR, name);
  await page.screenshot({ path, fullPage: true });
  console.log(`  captured: ${name}`);
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 640, height: 800 } });
  const page = await context.newPage();

  console.log(`Connecting to ${BASE_URL}...\n`);

  // Scenario 1: 첫 방문 — 빈 상태
  console.log("Scenario 1: 빈 상태");
  await page.goto(BASE_URL);
  await page.waitForSelector("#empty-state");
  await screenshot(page, "final-01-empty.png");

  // Scenario 2: 첫 할 일 추가
  console.log("Scenario 2: 첫 할 일 추가");
  await page.fill("#todo-input", "우유 사기");
  await page.press("#todo-input", "Enter");
  await page.waitForSelector(".todo-item");
  await screenshot(page, "final-02-first-todo.png");

  // Scenario 3: 여러 항목 추가
  console.log("Scenario 3: 여러 항목 추가");
  const items = ["빨래 돌리기", "이메일 확인", "운동하기"];
  for (const item of items) {
    await page.fill("#todo-input", item);
    await page.press("#todo-input", "Enter");
    await page.waitForTimeout(300);
  }
  await page.waitForTimeout(500);
  await screenshot(page, "final-03-multiple.png");

  // Scenario 4: 완료 토글
  console.log("Scenario 4: 완료 토글");
  const firstCheckbox = page.locator(".todo-checkbox").first();
  await firstCheckbox.click();
  await page.waitForTimeout(500);
  await screenshot(page, "final-04-completed.png");

  // Scenario 5: 완료 되돌리기
  console.log("Scenario 5: 완료 되돌리기");
  await firstCheckbox.click();
  await page.waitForTimeout(500);
  // 스크린샷 생략 (시나리오 3과 동일 상태)

  // Scenario 6: 인라인 편집
  console.log("Scenario 6: 인라인 편집");
  const secondTitle = page.locator(".todo-title").nth(1);
  await secondTitle.dblclick();
  await page.waitForSelector(".todo-edit-input");
  await page.fill(".todo-edit-input", "빨래 돌리고 널기");
  await page.press(".todo-edit-input", "Enter");
  await page.waitForTimeout(500);
  await screenshot(page, "final-05-edited.png");

  // Scenario 7: 삭제
  console.log("Scenario 7: 삭제");
  const lastItem = page.locator(".todo-item").last();
  await lastItem.hover();
  await page.waitForTimeout(300);
  const deleteBtn = lastItem.locator(".todo-delete");
  await deleteBtn.click();
  await page.waitForTimeout(800);
  await screenshot(page, "final-06-deleted.png");

  // Scenario 8: 빈 입력 거부
  console.log("Scenario 8: 빈 입력 거부");
  await page.fill("#todo-input", "");
  await page.press("#todo-input", "Enter");
  await page.waitForTimeout(500);
  await screenshot(page, "final-07-shake.png");

  // Scenario 9: 새로고침 후 데이터 유지
  console.log("Scenario 9: 새로고침 후 데이터 유지");
  await page.reload();
  await page.waitForSelector(".todo-item");
  await page.waitForTimeout(500);
  await screenshot(page, "final-08-after-refresh.png");

  await browser.close();
  console.log("\nAll scenarios completed.");
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
